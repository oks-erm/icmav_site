<!-- src/components/HelpRequest.vue -->

<template>
  <div class="max-w-7xl mx-auto px-4" data-aos="fade-up">
    <div class="max-w-6xl mx-auto">
      <div v-if="loading" class="text-center text-gray-500 py-8">
        A carregar...
      </div>

      <div v-else-if="error" class="text-center text-red-600 py-8">
        {{ error }}
      </div>

      <div v-else class="relative">
        <div class="relative z-20 flex justify-center">
          <div v-if="!showForm" class="flex flex-col sm:flex-row text-2xl justify-center gap-8 w-full">
            <button
              type="button"
              @click="openForm('prayer')"
              :class="[topActionButtonBaseClass, 'bg-info']"
            >
              Fazer Pedido de Oração
            </button>

            <button
              type="button"
              @click="openForm('counseling')"
              :class="[topActionButtonBaseClass, 'bg-green-500']"
            >
              Solicitar Aconselhamento Pastoral
            </button>
          </div>

          <button
            v-else
            type="button"
            :class="[topActionButtonBaseClass, 'text-2xl', formType === 'prayer' ? 'bg-info' : 'bg-green-500']"
            @click="closeForm"
          >
            {{ formType === 'prayer' ? 'Fazer Pedido de Oração' : 'Solicitar Aconselhamento Pastoral' }}
          </button>
        </div>

        <transition name="slide-fade">
          <div
            v-if="showForm"
            class="relative z-10 max-w-5xl mx-auto -mt-8 pt-16 pb-8 px-6 md:px-8 bg-white/95 backdrop-blur-md border border-white/60 rounded-[2rem] shadow-2xl"
          >
            <template v-if="step === 'form'">
              <div class="mb-8 text-center space-y-2">
                <p v-if="formType === 'prayer'" class="text-lg md:text-xl text-gray-900 font-medium">
                  Podemos orar por ti?
                </p>

                <p v-if="formType === 'prayer'" class="text-base text-gray-600">
                  Partilha connosco o teu pedido de oração.
                </p>

                <p v-if="formType === 'counseling'" class="text-lg md:text-xl text-gray-900 font-medium">
                  Precisas de ser ouvido/a e que alguém te aconselhe?
                </p>

                <p v-if="formType === 'counseling'" class="text-base text-gray-600">
                  Agenda uma conversa privada com alguém da nossa equipa pastoral.
                </p>
              </div>

              <form class="space-y-8" @submit.prevent="submitForm" novalidate>
                <div v-if="formType === 'prayer'" class="flex gap-3 overflow-x-auto pb-2 hide-scrollbar justify-center">
                  <button
                    type="button"
                    @click="changePrayerMode('identified')"
                    class="shrink-0 rounded-full px-5 py-2.5 text-sm md:text-base font-semibold transition-all duration-300 ease-out cursor-pointer"
                    :class="
                      form.prayerMode === 'identified'
                        ? 'bg-sky-700 text-white shadow-lg'
                        : 'bg-sky-50 text-sky-800 border border-sky-200'
                    "
                  >
                    Identificado
                  </button>

                  <button
                    type="button"
                    @click="changePrayerMode('anonymous')"
                    class="shrink-0 rounded-full px-5 py-2.5 text-sm md:text-base font-semibold transition-all duration-300 ease-out cursor-pointer"
                    :class="
                      form.prayerMode === 'anonymous'
                        ? 'bg-violet-700 text-white shadow-lg'
                        : 'bg-violet-50 text-violet-800 border border-violet-200'
                    "
                  >
                    Anónimo
                  </button>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                  <div v-if="requiresIdentityFields">
                    <label
                      for="hr-name"
                      class="block text-sm font-semibold mb-2"
                      :class="getLabelClass('name', true)"
                    >
                      Nome <span class="text-red-600">*</span>
                    </label>
                    <input
                      id="hr-name"
                      v-model="form.name"
                      type="text"
                      :class="getInputClass('name')"
                      @blur="markTouched('name')"
                      @input="validateField('name')"
                      required
                    />
                    <p v-if="showError('name')" class="mt-2 text-sm text-red-600">
                      {{ errors.name }}
                    </p>
                  </div>

                  <div v-if="requiresIdentityFields">
                    <label
                      class="block text-sm font-semibold mb-2"
                      :class="getLabelClass('phone', true)"
                    >
                      Telemóvel <span class="text-red-600">*</span>
                    </label>

                    <div
                      :class="[
                        'tel-field',
                        showError('phone') ? 'tel-field-error' : 'tel-field-normal'
                      ]"
                    >
                      <vue-tel-input
                        v-model="form.phone"
                        mode="auto"
                        :defaultCountry="'PT'"
                        :preferredCountries="['PT', 'BR', 'GB']"
                        :autoDefaultCountry="false"
                        :inputOptions="{
                          placeholder: 'Introduz o teu telemóvel',
                          required: requiresIdentityFields
                        }"
                        :dropdownOptions="{
                          showDialCodeInSelection: true,
                          showDialCodeInList: true,
                          showFlags: true,
                          showSearchBox: true
                        }"
                        validCharactersOnly
                        @country-changed="handleCountryChanged"
                        @validate="handlePhoneValidation"
                        @blur="markTouched('phone')"
                      />
                    </div>

                    <p v-if="showError('phone')" class="mt-2 text-sm text-red-600">
                      {{ errors.phone }}
                    </p>
                  </div>

                  <div class="md:col-span-2">
                    <label
                      for="hr-subject"
                      class="block text-sm font-semibold mb-2"
                      :class="getLabelClass('subject', true)"
                    >
                      Assunto <span class="text-red-600">*</span>
                    </label>
                    <textarea
                      id="hr-subject"
                      v-model="form.subject"
                      rows="5"
                      :class="getTextareaClass('subject')"
                      @blur="markTouched('subject')"
                      @input="validateField('subject')"
                      required
                    ></textarea>
                    <p v-if="showError('subject')" class="mt-2 text-sm text-red-600">
                      {{ errors.subject }}
                    </p>
                  </div>

                  <div class="md:col-span-2 relative" ref="pastorPickerRef">
                    <label
                      for="hr-pastor"
                      class="block text-sm font-semibold mb-2"
                      :class="getLabelClass('pastor', false)"
                    >
                      Pastor
                    </label>

                    <div
                      id="hr-pastor"
                      class="relative w-full rounded-2xl bg-white px-4 py-3 pr-20 text-left shadow-sm outline-none transition-all duration-200 border border-gray-200"
                      :class="showError('pastor') ? 'border-red-500 ring-4 ring-red-100' : 'focus-within:border-primary focus-within:ring-4 focus-within:ring-primary/10'"
                    >
                      <button
                        type="button"
                        class="w-full text-left cursor-pointer"
                        @click="togglePastorDropdown"
                        @blur="handlePastorBlur"
                      >
                        <span :class="form.pastor ? 'text-gray-900' : 'text-gray-400'">
                          {{ form.pastor || 'Escolhe um pastor (opcional)' }}
                        </span>
                      </button>

                      <span class="absolute inset-y-0 right-4 flex items-center gap-3 text-gray-400">
                        <button
                          v-if="form.pastor"
                          type="button"
                          class="text-gray-400 cursor-pointer"
                          @mousedown.prevent.stop="clearPastorSelection"
                          aria-label="Limpar pastor selecionado"
                        >
                          <i class="fas fa-times"></i>
                        </button>

                        <button
                          type="button"
                          class="cursor-pointer"
                          @mousedown.prevent="togglePastorDropdown"
                          aria-label="Abrir lista de pastores"
                        >
                          <i
                            class="fas fa-chevron-down text-sm transition-transform duration-200"
                            :class="showPastorDropdown ? 'rotate-180' : ''"
                          ></i>
                        </button>
                      </span>
                    </div>

                    <transition name="fade-scale">
                      <div
                        v-if="showPastorDropdown"
                        class="absolute z-30 mt-2 w-full overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-xl"
                      >
                        <div class="max-h-72 overflow-y-auto py-2">
                          <button
                            v-for="option in pastoralOptions"
                            :key="option"
                            type="button"
                            class="w-full px-4 py-3 text-left text-gray-900 transition-colors duration-200 cursor-pointer hover:bg-sky-50"
                            @mousedown.prevent="selectPastor(option)"
                          >
                            {{ option }}
                          </button>
                        </div>
                      </div>
                    </transition>

                    <p v-if="showError('pastor')" class="mt-2 text-sm text-red-600">
                      {{ errors.pastor }}
                    </p>
                  </div>

                  <div class="md:col-span-2">
                    <label class="flex items-start gap-3 cursor-pointer">
                      <input
                        v-model="form.consent"
                        type="checkbox"
                        class="mt-1 h-5 w-5 rounded border-gray-300 text-primary focus:ring-primary"
                        @change="markTouched('consent')"
                      />
                      <span
                        class="text-sm italic leading-relaxed"
                        :class="showError('consent') ? 'text-red-600' : 'text-gray-600'"
                      >
                        Autorizo a ICMAV a recolher e tratar os meus dados pessoais apenas para este pedido, e confirmo que não serão partilhados com terceiros sem o meu consentimento.
                      </span>
                    </label>

                    <p v-if="showError('consent')" class="mt-2 text-sm text-red-600">
                      {{ errors.consent }}
                    </p>
                  </div>
                </div>

                <div class="flex flex-col sm:flex-row justify-center gap-3 pt-2">
                  <button
                    type="submit"
                    class="w-full sm:w-52 rounded-full bg-primary px-8 py-4 font-semibold text-white shadow-lg transition-all duration-300 cursor-pointer"
                  >
                    Submeter
                  </button>

                  <button
                    @click="closeForm"
                    type="button"
                    class="w-full sm:w-52 rounded-full bg-red-600 px-8 py-4 font-semibold text-white shadow-lg transition-all duration-300 cursor-pointer"
                  >
                    Cancelar
                  </button>
                </div>
              </form>
            </template>

            <template v-else>
              <div class="max-w-3xl mx-auto text-center py-6 space-y-6">
                <p class="text-2xl md:text-3xl font-semibold text-gray-900">
                  Obrigado pelo teu contacto.
                </p>

                <p class="text-base md:text-lg text-gray-600 leading-relaxed">
                  Recebemos o teu pedido e vamos estar contigo. Deus te abençoe.
                </p>

                <div class="flex justify-center pt-2">
                  <button
                    @click="closeForm"
                    type="button"
                    class="w-full sm:w-52 rounded-full bg-primary px-8 py-4 font-semibold text-white shadow-lg transition-all duration-300 cursor-pointer"
                  >
                    Fechar
                  </button>
                </div>
              </div>
            </template>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { getPastoralTeamContent } from '../services/api'

const loading = ref(true)
const error = ref('')
const showForm = ref(false)
const step = ref('form')
const formType = ref('')
const showPastorDropdown = ref(false)
const pastorPickerRef = ref(null)
const pastoralOptions = ref([])

const form = ref({
  prayerMode: 'identified',
  name: '',
  phone: '',
  subject: '',
  pastor: '',
  consent: false,
})

const phoneMeta = ref({
  valid: false,
  number: '',
  country: null,
})

const touched = ref({
  name: false,
  phone: false,
  subject: false,
  pastor: false,
  consent: false,
})

const errors = ref({
  name: '',
  phone: '',
  subject: '',
  pastor: '',
  consent: '',
})

const requiresIdentityFields = computed(() => {
  return formType.value === 'counseling' || form.value.prayerMode === 'identified'
})

const topActionButtonBaseClass =
  'w-full sm:w-auto rounded-full px-8 py-4 font-semibold text-white shadow-lg transition-all duration-300 cursor-pointer'

function resetForm() {
  form.value = {
    prayerMode: 'identified',
    name: '',
    phone: '',
    subject: '',
    pastor: '',
    consent: false,
  }

  phoneMeta.value = {
    valid: false,
    number: '',
    country: null,
  }

  touched.value = {
    name: false,
    phone: false,
    subject: false,
    pastor: false,
    consent: false,
  }

  errors.value = {
    name: '',
    phone: '',
    subject: '',
    pastor: '',
    consent: '',
  }

  showPastorDropdown.value = false
  step.value = 'form'
}

function openForm(type) {
  formType.value = type
  resetForm()
  showForm.value = true
}

function closeForm() {
  resetForm()
  showForm.value = false
  formType.value = ''
}

function changePrayerMode(mode) {
  form.value.prayerMode = mode

  if (mode === 'anonymous') {
    form.value.name = ''
    form.value.phone = ''
    errors.value.name = ''
    errors.value.phone = ''
    touched.value.name = false
    touched.value.phone = false
    phoneMeta.value = {
      valid: false,
      number: '',
      country: null,
    }
  }
}

function togglePastorDropdown() {
  showPastorDropdown.value = !showPastorDropdown.value
}

function selectPastor(option) {
  form.value.pastor = option
  touched.value.pastor = true
  validateField('pastor')
  showPastorDropdown.value = false
}

function handlePastorBlur() {
  touched.value.pastor = true
  validateField('pastor')

  setTimeout(() => {
    showPastorDropdown.value = false
  }, 150)
}

function handleClickOutside(event) {
  if (pastorPickerRef.value && !pastorPickerRef.value.contains(event.target)) {
    showPastorDropdown.value = false
  }
}

function handleCountryChanged(country) {
  phoneMeta.value.country = country || null
  validateField('phone')
}

function handlePhoneValidation(payload) {
  phoneMeta.value = {
    valid: !!payload?.valid,
    number: payload?.number || '',
    country: payload?.country || phoneMeta.value.country || null,
  }

  validateField('phone')
}

function validateField(field) {
  const value = String(form.value[field] ?? '').trim()

  if (field === 'name') {
    if (!requiresIdentityFields.value) {
      errors.value.name = ''
    } else {
      errors.value.name = value ? '' : 'O campo Nome é obrigatório.'
    }
    return
  }

  if (field === 'phone') {
    if (!requiresIdentityFields.value) {
      errors.value.phone = ''
    } else if (!String(form.value.phone || '').trim()) {
      errors.value.phone = 'O campo Telemóvel é obrigatório.'
    } else if (!phoneMeta.value.valid) {
      errors.value.phone = 'Introduz um telemóvel válido para o país selecionado.'
    } else {
      errors.value.phone = ''
    }
    return
  }

  if (field === 'subject') {
    errors.value.subject = value ? '' : 'O campo Assunto é obrigatório.'
    return
  }

  if (field === 'pastor') {
    errors.value.pastor = ''
    return
  }

  if (field === 'consent') {
    errors.value.consent = form.value.consent
      ? ''
      : 'Tens de autorizar o tratamento dos dados para continuar.'
  }
}

function markTouched(field) {
  touched.value[field] = true
  validateField(field)
}

function showError(field) {
  return touched.value[field] && !!errors.value[field]
}

function getInputClass(field) {
  return [
    'w-full rounded-2xl bg-white px-4 py-3 text-gray-900 shadow-sm outline-none transition-all duration-200',
    showError(field)
      ? 'border border-red-500 ring-4 ring-red-100'
      : 'border border-gray-200 hover:border-gray-300 focus:border-primary focus:ring-4 focus:ring-primary/10'
  ]
}

function getTextareaClass(field) {
  return [
    'w-full rounded-2xl bg-white px-4 py-3 text-gray-900 shadow-sm outline-none transition-all duration-200 resize-y min-h-[120px]',
    showError(field)
      ? 'border border-red-500 ring-4 ring-red-100'
      : 'border border-gray-200 hover:border-gray-300 focus:border-primary focus:ring-4 focus:ring-primary/10'
  ]
}

function getLabelClass(field, required = false) {
  if (required && showError(field)) {
    return 'text-red-600'
  }

  return 'text-gray-700'
}

function validateForm() {
  const fieldsToCheck = ['subject', 'consent']

  if (requiresIdentityFields.value) {
    fieldsToCheck.unshift('name', 'phone')
  }

  fieldsToCheck.forEach((field) => {
    touched.value[field] = true
    validateField(field)
  })

  return fieldsToCheck.every((field) => !errors.value[field])
}

function submitForm() {
  if (!validateForm()) return

  step.value = 'success'
}

function clearPastorSelection() {
  form.value.pastor = ''
  touched.value.pastor = false
  errors.value.pastor = ''
  showPastorDropdown.value = false
}

async function loadPastoralTeam() {
  loading.value = true
  error.value = ''

  try {
    const data = await getPastoralTeamContent()
    const list = Array.isArray(data.value) ? data.value : []
    pastoralOptions.value = list
      .map(item => String(item?.name || '').trim())
      .filter(Boolean)
  } catch (err) {
    error.value = err.message || 'Não foi possível carregar este conteúdo neste momento.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  loadPastoralTeam()
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.hide-scrollbar {
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.hide-scrollbar::-webkit-scrollbar {
  display: none;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.25s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-fade-enter-to,
.slide-fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.18s ease;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: translateY(-6px) scale(0.98);
}

.fade-scale-enter-to,
.fade-scale-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.tel-field {
  width: 100%;
}

.tel-field :deep(.vue-tel-input) {
  width: 100%;
  display: flex;
  align-items: stretch;
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  outline: none !important;
  transition: all 0.2s ease;
}

.tel-field :deep(.vue-tel-input:focus-within) {
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
}

.tel-field :deep(.vti__dropdown) {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-inline: 0.85rem;
  background: #ffffff !important;
  border: 1px solid #e5e7eb !important;
  border-right: 1px solid #e5e7eb !important;
  border-radius: 1rem 0 0 1rem !important;
  box-shadow: none !important;
  outline: none !important;
  transition: background-color 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.tel-field :deep(.vti__dropdown:hover) {
  background: #f9fafb !important;
  border-color: #d1d5db !important;
}

.tel-field :deep(.vti__selection) {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.tel-field :deep(.vti__input) {
  width: 100%;
  min-height: 50px;
  background: #ffffff !important;
  color: #111827 !important;
  border: 1px solid #e5e7eb !important;
  border-left: 0 !important;
  border-radius: 0 1rem 1rem 0 !important;
  box-shadow: none !important;
  outline: none !important;
  padding: 0.75rem 1rem !important;
  text-align: left !important;
  direction: ltr !important;
  transition: background-color 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}

.tel-field :deep(.vti__input:hover) {
  border-color: #d1d5db !important;
  background: #fcfcfc !important;
}

.tel-field :deep(.vti__input:focus) {
  outline: none !important;
  box-shadow: none !important;
}

.tel-field :deep(.vti__input::placeholder) {
  color: #9ca3af;
  text-align: left;
}

.tel-field :deep(.vti__dropdown-list) {
  border-radius: 1rem;
  border: 1px solid #e5e7eb;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
}

.tel-field :deep(.vti__search_box) {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  outline: none;
  box-shadow: none;
}

.tel-field-normal :deep(.vti__dropdown),
.tel-field-normal :deep(.vti__input) {
  border-color: #e5e7eb !important;
}

.tel-field-normal :deep(.vue-tel-input:hover .vti__dropdown),
.tel-field-normal :deep(.vue-tel-input:hover .vti__input) {
  border-color: #d1d5db !important;
}

.tel-field-normal :deep(.vue-tel-input:focus-within .vti__dropdown),
.tel-field-normal :deep(.vue-tel-input:focus-within .vti__input) {
  border-color: rgb(59 130 246) !important;
  box-shadow: 0 0 0 4px rgb(59 130 246 / 0.10) !important;
}

.tel-field-error :deep(.vti__dropdown),
.tel-field-error :deep(.vti__input) {
  border-color: rgb(239 68 68) !important;
}

.tel-field-error :deep(.vue-tel-input:hover .vti__dropdown),
.tel-field-error :deep(.vue-tel-input:hover .vti__input) {
  border-color: rgb(239 68 68) !important;
}

.tel-field-error :deep(.vue-tel-input:focus-within .vti__dropdown),
.tel-field-error :deep(.vue-tel-input:focus-within .vti__input) {
  border-color: rgb(239 68 68) !important;
  box-shadow: 0 0 0 4px rgb(239 68 68 / 0.10) !important;
}
</style>
