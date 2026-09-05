<!-- src/components/LocalGatherings.vue -->

<template>
  <div class="mx-auto px-4 space-y-6" data-aos="fade-up">
    <div v-if="loading" class="text-center text-gray-500">
      A carregar conteúdo...
    </div>

    <div v-else-if="error" class="text-center text-red-600">
      {{ error }}
    </div>

    <div v-else class="space-y-6">
      <blockquote class="max-w-3xl mx-auto text-center italic border-l-4 border-info pl-4">
        “{{ content.localGatheringsQuote }}”<br />
        <span class="font-medium">— {{ content.localGatheringsQuoteReference }} —</span>
      </blockquote>

      <div class="max-w-6xl mx-auto text-center space-y-2" v-html="content.localGatheringsBody"></div>
    </div>

    <div class="relative pt-10">
      <div class="relative z-20 flex justify-center px-4">
        <div v-if="!showForm" class="w-full max-w-sm sm:max-w-none flex justify-center">
          <button
            @click="openForm"
            id="join"
            class="btn btn-info rounded-full min-h-[3.25rem] md:btn-xl py-3.5 md:py-4 px-6 md:px-12 shadow-lg transition-all duration-300 cursor-pointer text-center leading-snug w-full sm:w-auto"
          >
            Junta-te a um Pequeno Grupo
          </button>
        </div>
        <div v-else class="w-full max-w-sm sm:max-w-none flex justify-center">
          <button
            @click="closeForm"
            id="join"
            class="btn btn-info rounded-full min-h-[3.25rem] md:btn-xl py-3.5 md:py-4 px-6 md:px-12 shadow-lg transition-all duration-300 cursor-pointer text-center leading-snug w-full sm:w-auto"
          >
            Junta-te a um Pequeno Grupo
          </button>
        </div>
      </div>

      <transition name="slide-fade">
        <div
          v-if="showForm"
          class="relative z-10 max-w-5xl mx-auto -mt-8 pt-16 pb-8 px-6 md:px-8 bg-white/95 backdrop-blur-md border border-white/60 rounded-[2rem] shadow-2xl"
        >
          <template v-if="step === 'form'">
            <form class="space-y-8" @submit.prevent="submitForm" novalidate>
              <div class="flex flex-col sm:flex-row gap-2.5 sm:gap-3 justify-center max-w-md sm:max-w-none mx-auto">
                <button
                  type="button"
                  @click="changeMode('recommend')"
                  class="w-full sm:w-auto shrink-0 rounded-full px-5 py-2.5 text-sm md:text-base font-semibold transition-all duration-300 ease-out cursor-pointer text-center"
                  :class="
                    form.mode === 'recommend'
                      ? 'bg-sky-700 text-white shadow-lg'
                      : 'bg-sky-50 text-sky-800 border border-sky-200'
                  "
                >
                  Ajudem-me a escolher
                </button>

                <button
                  type="button"
                  @click="changeMode('choose')"
                  class="w-full sm:w-auto shrink-0 rounded-full px-5 py-2.5 text-sm md:text-base font-semibold transition-all duration-300 ease-out cursor-pointer text-center"
                  :class="
                    form.mode === 'choose'
                      ? 'bg-violet-700 text-white shadow-lg'
                      : 'bg-violet-50 text-violet-800 border border-violet-200'
                  "
                >
                  Eu escolho!
                </button>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                <div v-if="form.mode === 'choose'" class="md:col-span-2 relative" ref="groupPickerRef">
                  <label
                    for="lg-choice"
                    class="block text-sm font-semibold mb-2"
                    :class="getLabelClass('selectedGroupLabel', true)"
                  >
                    Escolher Pequeno Grupo <span class="text-red-600">*</span>
                  </label>

                  <button
                    id="lg-choice"
                    type="button"
                    class="relative w-full rounded-2xl bg-white px-4 py-3 text-left shadow-sm outline-none transition-all duration-200 cursor-pointer"
                    :class="
                      showError('selectedGroupLabel')
                        ? 'border border-red-500 ring-4 ring-red-100'
                        : 'border border-gray-200 focus:border-primary focus:ring-4 focus:ring-primary/10'
                    "
                    @click="toggleGroupDropdown"
                    @blur="handleGroupButtonBlur"
                  >
                    <span :class="form.selectedGroupLabel ? 'text-gray-900' : 'text-gray-400'">
                      {{ form.selectedGroupLabel || 'Escolhe pelo líder, característica ou local' }}
                    </span>

                    <span class="absolute inset-y-0 right-4 flex items-center text-gray-400">
                      <i
                        class="fas fa-chevron-down text-sm transition-transform duration-200"
                        :class="showGroupDropdown ? 'rotate-180' : ''"
                      ></i>
                    </span>
                  </button>

                  <transition name="fade-scale">
                    <div
                      v-if="showGroupDropdown"
                      class="absolute z-30 mt-2 w-full overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-xl"
                    >
                      <div class="max-h-72 overflow-y-auto py-2">
                        <button
                          v-for="option in groupOptions"
                          :key="option.slug"
                          type="button"
                          class="w-full px-4 py-3 text-left transition-colors duration-200 cursor-pointer hover:bg-sky-50"
                          @mousedown.prevent="selectGroupOption(option)"
                        >
                          <div class="font-semibold text-gray-900">
                            {{ option.leaderName }}
                          </div>
                          <div class="text-sm text-gray-500">
                            {{ option.characteristicTag }} · {{ option.location }}
                          </div>
                        </button>
                      </div>
                    </div>
                  </transition>

                  <p v-if="showError('selectedGroupLabel')" class="mt-2 text-sm text-red-600">
                    {{ errors.selectedGroupLabel }}
                  </p>
                </div>

                <div>
                  <label
                    for="lg-name"
                    class="block text-sm font-semibold mb-2"
                    :class="getLabelClass('name', true)"
                  >
                    Nome <span class="text-red-600">*</span>
                  </label>
                  <input
                    id="lg-name"
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

                <div>
                  <label
                    for="lg-age"
                    class="block text-sm font-semibold mb-2"
                    :class="getLabelClass('age', true)"
                  >
                    Idade <span class="text-red-600">*</span>
                  </label>
                  <input
                    id="lg-age"
                    v-model="form.age"
                    type="text"
                    inputmode="numeric"
                    pattern="[0-9]*"
                    :class="getInputClass('age')"
                    @blur="markTouched('age')"
                    @input="handleDigitsOnlyInput('age')"
                    required
                  />
                  <p v-if="showError('age')" class="mt-2 text-sm text-red-600">
                    {{ errors.age }}
                  </p>
                </div>

                <div class="relative" ref="maritalStatusPickerRef">
                    <label
                        for="lg-marital-status"
                        class="block text-sm font-semibold mb-2"
                        :class="getLabelClass('maritalStatus', true)"
                    >
                        Estado Civil <span class="text-red-600">*</span>
                    </label>

                    <button
                        id="lg-marital-status"
                        type="button"
                        class="relative w-full rounded-2xl bg-white px-4 py-3 text-left shadow-sm outline-none transition-all duration-200 cursor-pointer"
                        :class="
                        showError('maritalStatus')
                            ? 'border border-red-500 ring-4 ring-red-100'
                            : 'border border-gray-200 focus:border-primary focus:ring-4 focus:ring-primary/10'
                        "
                        @click="toggleMaritalStatusDropdown"
                        @blur="handleMaritalStatusBlur"
                    >
                        <span :class="form.maritalStatus ? 'text-gray-900' : 'text-gray-400'">
                            {{ form.maritalStatus || 'Escolhe o estado civil' }}
                        </span>

                        <span class="absolute inset-y-0 right-4 flex items-center text-gray-400">
                            <i
                                class="fas fa-chevron-down text-sm transition-transform duration-200"
                                :class="showMaritalStatusDropdown ? 'rotate-180' : ''"
                            ></i>
                        </span>
                    </button>

                    <transition name="fade-scale">
                        <div
                        v-if="showMaritalStatusDropdown"
                        class="absolute z-30 mt-2 w-full overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-xl"
                        >
                            <div class="py-2">
                                <button
                                v-for="option in maritalStatusOptions"
                                :key="option"
                                type="button"
                                class="w-full px-4 py-3 text-left text-gray-900 transition-colors duration-200 cursor-pointer hover:bg-sky-50"
                                @mousedown.prevent="selectMaritalStatus(option)"
                                >
                                {{ option }}
                                </button>
                            </div>
                        </div>
                    </transition>

                    <p v-if="showError('maritalStatus')" class="mt-2 text-sm text-red-600">
                        {{ errors.maritalStatus }}
                    </p>
                </div>

                <div>
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
                      :preferredCountries="['PT', 'GB', 'FR', 'CH', 'LU']"
                      :autoDefaultCountry="false"
                      :inputOptions="{
                        placeholder: 'Introduz o teu telemóvel',
                        required: true
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
                    for="lg-email"
                    class="block text-sm font-semibold mb-2"
                    :class="getLabelClass('email', true)"
                  >
                    E-mail <span class="text-red-600">*</span>
                  </label>
                  <input
                    id="lg-email"
                    v-model="form.email"
                    type="email"
                    autocomplete="email"
                    :class="getInputClass('email')"
                    @blur="markTouched('email')"
                    @input="validateField('email')"
                    required
                  />
                  <p v-if="showError('email')" class="mt-2 text-sm text-red-600">
                    {{ errors.email }}
                  </p>
                </div>

                <div v-if="form.mode === 'recommend'" class="md:col-span-2">
                  <label
                    for="lg-address"
                    class="block text-sm font-semibold mb-2"
                    :class="getLabelClass('address', true)"
                  >
                    Morada <span class="text-red-600">*</span>
                  </label>
                  <input
                    id="lg-address"
                    v-model="form.address"
                    type="text"
                    :class="getInputClass('address')"
                    @blur="markTouched('address')"
                    @input="validateField('address')"
                    required
                  />
                  <p v-if="showError('address')" class="mt-2 text-sm text-red-600">
                    {{ errors.address }}
                  </p>
                </div>
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

              <div class="flex flex-col sm:flex-row justify-center gap-3 pt-2">
                <button
                  type="submit"
                  class="w-full sm:w-52 rounded-full bg-primary px-8 py-4 font-semibold text-white shadow-lg transition-all duration-300 cursor-pointer"
                >
                  Inscrever
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
                Estarmos juntos vai ser espétacular!
              </p>

              <div class="text-base md:text-lg text-gray-600 leading-relaxed space-y-2">
                <p>Estarmos perto é tão importante para ti como para mim. É importante para nós, para a ICMAV e para Deus.</p>
                <p>Enviámos a tua inscrição para os responsáveis dos pequenos grupos, vamos entrar em contacto contigo em breve. Fica atento.</p>
              </div>

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
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { getLocalGatheringsContent, getLocalGatheringOptions } from '../services/api'

const loading = ref(true)
const error = ref('')
const content = ref({
  quote: '',
  author: '',
  body: '',
})

const showForm = ref(false)
const step = ref('form')
const groupOptions = ref([])
const showGroupDropdown = ref(false)
const groupPickerRef = ref(null)

const form = ref({
  mode: 'recommend',
  name: '',
  age: '',
  maritalStatus: '',
  phone: '',
  email: '',
  address: '',
  selectedGroupLabel: '',
  consent: false,
})

const phoneMeta = ref({
  valid: false,
  number: '',
  country: null,
})

const touched = ref({
  name: false,
  age: false,
  maritalStatus: false,
  phone: false,
  email: false,
  address: false,
  selectedGroupLabel: false,
  consent: false,
})

const errors = ref({
  name: '',
  age: '',
  maritalStatus: '',
  phone: '',
  email: '',
  address: '',
  selectedGroupLabel: '',
  consent: '',
})

const maritalStatusOptions = [
  'Solteiro/a',
  'Casado/a',
  'Viúvo/a',
  'Divorciado/a',
  'Prefiro não dizer',
]

const showMaritalStatusDropdown = ref(false)
const maritalStatusPickerRef = ref(null)

function formatOptionLabel(option) {
  return `${option.leaderName} — ${option.characteristicTag} — ${option.location}`
}

function resetForm() {
  form.value = {
    mode: 'recommend',
    name: '',
    age: '',
    maritalStatus: '',
    phone: '',
    email: '',
    address: '',
    selectedGroupLabel: '',
    consent: false,
  }

  phoneMeta.value = {
    valid: false,
    number: '',
    country: null,
  }

  touched.value = {
    name: false,
    age: false,
    maritalStatus: false,
    phone: false,
    email: false,
    address: false,
    selectedGroupLabel: false,
    consent: false,
  }

  errors.value = {
    name: '',
    age: '',
    maritalStatus: '',
    phone: '',
    email: '',
    address: '',
    selectedGroupLabel: '',
    consent: false,
  }

  showGroupDropdown.value = false
  showMaritalStatusDropdown.value = false
  step.value = 'form'
}

function openForm() {
  if (showForm.value) return
  resetForm()
  showForm.value = true
}

function closeForm() {
  resetForm()
  showForm.value = false
}

function changeMode(mode) {
  form.value.mode = mode
  errors.value.address = ''
  errors.value.selectedGroupLabel = ''
  touched.value.address = false
  touched.value.selectedGroupLabel = false
  form.value.selectedGroupLabel = ''
  showGroupDropdown.value = false
  showMaritalStatusDropdown.value = false
}

function toggleGroupDropdown() {
  showGroupDropdown.value = !showGroupDropdown.value
}

function selectGroupOption(option) {
  const label = formatOptionLabel(option)
  form.value.selectedGroupLabel = label
  touched.value.selectedGroupLabel = true
  validateField('selectedGroupLabel')
  showGroupDropdown.value = false
}

function handleGroupButtonBlur() {
  touched.value.selectedGroupLabel = true
  validateField('selectedGroupLabel')

  setTimeout(() => {
    showGroupDropdown.value = false
  }, 150)
}

function handleClickOutside(event) {
  if (groupPickerRef.value && !groupPickerRef.value.contains(event.target)) {
    showGroupDropdown.value = false
  }

  if (maritalStatusPickerRef.value && !maritalStatusPickerRef.value.contains(event.target)) {
    showMaritalStatusDropdown.value = false
  }
}

function handleDigitsOnlyInput(field) {
  form.value[field] = String(form.value[field]).replace(/\D/g, '')
  validateField(field)
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

function isEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
}

function isPositiveInteger(value) {
  return /^[0-9]+$/.test(value) && Number(value) > 0
}

function validateField(field) {
  const value = String(form.value[field] ?? '').trim()

  if (field === 'name') {
    errors.value.name = value ? '' : 'O campo Nome é obrigatório.'
    return
  }

  if (field === 'age') {
    if (!value) {
      errors.value.age = 'O campo Idade é obrigatório.'
    } else if (!isPositiveInteger(value)) {
      errors.value.age = 'Introduz uma idade válida.'
    } else {
      errors.value.age = ''
    }
    return
  }

  if (field === 'maritalStatus') {
    errors.value.maritalStatus = value ? '' : 'O campo Estado Civil é obrigatório.'
    return
  }

  if (field === 'phone') {
    if (!String(form.value.phone || '').trim()) {
      errors.value.phone = 'O campo Telemóvel é obrigatório.'
    } else if (!phoneMeta.value.valid) {
      errors.value.phone = 'Introduz um telemóvel válido para o país selecionado.'
    } else {
      errors.value.phone = ''
    }
    return
  }

  if (field === 'email') {
    if (!value) {
      errors.value.email = 'O campo E-mail é obrigatório.'
    } else if (!isEmail(value)) {
      errors.value.email = 'Introduz um e-mail válido.'
    } else {
      errors.value.email = ''
    }
    return
  }

  if (field === 'address') {
    if (form.value.mode === 'recommend') {
      errors.value.address = value ? '' : 'O campo Morada é obrigatório.'
    } else {
      errors.value.address = ''
    }
    return
  }

  if (field === 'selectedGroupLabel') {
    if (form.value.mode === 'choose') {
      errors.value.selectedGroupLabel = value ? '' : 'Escolhe um Pequeno Grupo.'
    } else {
      errors.value.selectedGroupLabel = ''
    }
  }

  if (field === 'consent') {
    errors.value.consent = form.value.consent
      ? ''
      : 'Tens de autorizar o tratamento dos dados para continuar.'
    return
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

function getLabelClass(field, required = false) {
  if (required && showError(field)) {
    return 'text-red-600'
  }

  return 'text-gray-700'
}

function validateForm() {
  const fieldsToCheck = ['name', 'age', 'maritalStatus', 'phone', 'email', 'consent']

  if (form.value.mode === 'recommend') {
    fieldsToCheck.push('address')
  }

  if (form.value.mode === 'choose') {
    fieldsToCheck.unshift('selectedGroupLabel')
  }

  fieldsToCheck.forEach((field) => {
    touched.value[field] = true
    validateField(field)
  })

  return fieldsToCheck.every((field) => !errors.value[field])
}

function submitForm() {
  if (!validateForm()) return

  const payload = {
    mode: form.value.mode,
    name: form.value.name.trim(),
    age: form.value.age.trim(),
    maritalStatus: form.value.maritalStatus.trim(),
    phone: phoneMeta.value.number || form.value.phone,
    phoneCountryCode: phoneMeta.value.country?.code || 'PT',
    phoneDialCode: phoneMeta.value.country?.dialCode || '+351',
    email: form.value.email.trim(),
    address: form.value.mode === 'recommend' ? form.value.address.trim() : null,
    selectedGroupLabel: form.value.mode === 'choose' ? form.value.selectedGroupLabel.trim() : null,
    consent: form.value.consent,
  }

  console.log('Local gathering form payload:', payload)
  step.value = 'success'
}

function toggleMaritalStatusDropdown() {
  showMaritalStatusDropdown.value = !showMaritalStatusDropdown.value
}

function selectMaritalStatus(option) {
  form.value.maritalStatus = option
  touched.value.maritalStatus = true
  validateField('maritalStatus')
  showMaritalStatusDropdown.value = false
}

function handleMaritalStatusBlur() {
  touched.value.maritalStatus = true
  validateField('maritalStatus')

  setTimeout(() => {
    showMaritalStatusDropdown.value = false
  }, 150)
}

onMounted(async () => {
  document.addEventListener('click', handleClickOutside)

  try {
    const [contentData, optionsData] = await Promise.all([
      getLocalGatheringsContent(),
      getLocalGatheringOptions(),
    ])

    content.value = contentData.value
    groupOptions.value = Array.isArray(optionsData.value) ? optionsData.value : []
  } catch (err) {
    error.value = err.message || 'Não foi possível carregar este conteúdo neste momento.'
  } finally {
    loading.value = false
  }
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