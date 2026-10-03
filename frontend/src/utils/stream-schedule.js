// src/utils/stream-schedule.js

/**
 * Each entry represents a weekly time window when the church goes live.
 *
 * - `day` is 0–6 (0 = Sunday, 1 = Monday, … 6 = Saturday).
 * - `startHour`, `startMin`, `endHour`, and `endMin` are in 24-hour format, Europe/Lisbon time.
 */
export const streamWindows = [
    {
        day: 0,        // Sunday
        startHour: 10, // 10:25
        startMin: 25,
        endHour: 12,   // 12:35
        endMin: 35
    },
    // …you can add more windows here if needed…
]
  