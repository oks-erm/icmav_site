<template>
    <div class="text-center">
        <!-- While we’re initializing, show nothing (or a spinner) -->
        <div v-if="loading" class="py-8">
            <span class="text-gray-500">Verificando horário de transmissão…</span>
        </div>

        <!-- If it’s currently within a streaming window, show the YouTube embed -->
        <div v-else-if="isLive" class="mx-auto w-full max-w-4xl">
            <div class="aspect-w-16 aspect-h-9">
                <iframe :src="youtubeEmbedUrl" frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen class="w-full h-full rounded-lg shadow-lg"></iframe>
            </div>
        </div>

        <!-- If not live, show when the next stream starts -->
        <div v-else class="py-8">
            <p class="text-gray-600">
                Próxima transmissão ao vivo:
                <span class="font-semibold">{{ nextWindowText }}</span>
            </p>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { streamWindows } from '../utils/stream-schedule.js'

// Replace with your channel’s live‐embed URL (if known), or if you know the live video ID:
const CHANNEL_ID = '' 

// If you know the live video ID (it never changes), you can hardcode it:
const LIVE_VIDEO_ID = '' 
// Otherwise, you could still fetch from the Data API here, but this example assumes fixed schedule.
const youtubeEmbedUrl = `https://www.youtube.com/embed/${LIVE_VIDEO_ID}?autoplay=1&rel=0`

// Reactive state
const loading = ref(true)
const isLive = ref(false)      // true if the current time falls in a stream window
const nextWindowText = ref('') // human‐friendly text for the next scheduled window

let timerHandle = null

/**
 * Check whether “now” in Europe/Lisbon falls inside any of the defined stream windows.
 * Also calculate the next upcoming window to display if not live.
 */
function checkSchedule() {
    const now = new Date()

    // Convert “now” to Europe/Lisbon time by using toLocaleString,
    // then reconstruct a Date object in that timezone:
    // (This is a common trick since JS Date always keeps things in UTC and local system time.)
    const lisbonString = now.toLocaleString('pt-PT', { timeZone: 'Europe/Lisbon' })
    const lisbonDate = new Date(lisbonString)

    const currentDay = lisbonDate.getDay()    // 0 = Sunday, … 6 = Saturday
    const currentHour = lisbonDate.getHours()
    const currentMin = lisbonDate.getMinutes()

    // First: see if we’re within any window
    let insideAny = false
    for (const window of streamWindows) {
        if (window.day === currentDay) {
            const startsAfter =
                currentHour > window.startHour ||
                (currentHour === window.startHour && currentMin >= window.startMin)
            const endsBefore =
                currentHour < window.endHour ||
                (currentHour === window.endHour && currentMin < window.endMin)

            if (startsAfter && endsBefore) {
                insideAny = true
                break
            }
        }
    }

    isLive.value = insideAny
    loading.value = false

    // If not live, compute next upcoming window (in Lisbon time)
    if (!insideAny) {
        // Build a list of “Date objects” for each window in the current week (or next week)
        const upcoming = []

        // Today’s midnight in Lisbon
        const todayLisbonMidnight = new Date(lisbonDate)
        todayLisbonMidnight.setHours(0, 0, 0, 0)

        for (let offset = 0; offset < 7; offset++) {
            const checkDay = (currentDay + offset) % 7
            // Base date = today’s midnight + offset days
            const base = new Date(todayLisbonMidnight)
            base.setDate(base.getDate() + offset)

            // For each window in streamWindows, if its day matches checkDay, build a Date
            for (const window of streamWindows) {
                if (window.day === checkDay) {
                    const startDt = new Date(base) // copy
                    startDt.setHours(window.startHour, window.startMin, 0, 0)
                    upcoming.push(startDt)
                }
            }
        }

        // Sort upcoming dates ascending
        upcoming.sort((a, b) => a.getTime() - b.getTime())

        // Pick the first date that’s strictly in the future (compared to lisbonDate)
        const next = upcoming.find((dt) => dt.getTime() > lisbonDate.getTime())
        if (next) {
            // Format “next” into something like: “Domingo, 18:00”
            const dayNames = [
                'Domingo',
                'Segunda-feira',
                'Terça-feira',
                'Quarta-feira',
                'Quinta-feira',
                'Sexta-feira',
                'Sábado'
            ]
            const dayName = dayNames[next.getDay()]
            const h = String(next.getHours()).padStart(2, '0')
            const m = String(next.getMinutes()).padStart(2, '0')
            nextWindowText.value = `${dayName} às ${h}:${m}`
        } else {
            // If nothing found (shouldn’t happen, unless streamWindows is empty)
            nextWindowText.value = 'Agendado em breve'
        }
    }
}

onMounted(() => {
    // Do the first check immediately
    checkSchedule()

    // Then set an interval: check every minute
    timerHandle = setInterval(checkSchedule, 60 * 1000)
})

onBeforeUnmount(() => {
    if (timerHandle) clearInterval(timerHandle)
})
</script>

<style scoped>
/* If you have Tailwind’s aspect-ratio plugin, you can use `aspect-w-16 aspect-h-9` instead: */
.aspect-w-16 {
    position: relative;
    width: 100%;
  }
  .aspect-w-16::before {
    content: '';
    display: block;
    padding-bottom: 56.25%;
  }
  .aspect-h-9 > iframe {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
  }
</style>
  
