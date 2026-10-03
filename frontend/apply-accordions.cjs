const fs = require('fs');
const file = 'src/views/AdminView.vue';
let content = fs.readFileSync(file, 'utf-8');

const scriptAdd = `const openSections = ref({
  welcome: false,
  message: false,
  purposes: false,
  pastoralTeam: false,
  ministries: false,
  servicesBanner: false,
  localGatherings: false,
  localGatheringOptions: false,
  gallery: false,
  socialMedia: false,
  donations: false,
  locations: false,
})

function toggleSection(section) {
  openSections.value[section] = !openSections.value[section]
}
function openAllSections() {
  Object.keys(openSections.value).forEach(k => openSections.value[k] = true)
}
function closeAllSections() {
  Object.keys(openSections.value).forEach(k => openSections.value[k] = false)
}
`;

content = content.replace('// ─── Section data refs ────────────────────────────────────────────────────────', '// ─── Section data refs ────────────────────────────────────────────────────────\n' + scriptAdd);

const cssAdd = `
.global-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.section-container {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.section-header, .group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: #f9fafb;
  margin-top: 0 !important;
  user-select: none;
  cursor: pointer;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 600;
  color: #374151;
  font-size: 1.05rem;
}

.section-title i {
  transition: transform 0.3s;
}

.section-title .rotate-180 {
  transform: rotate(-180deg);
}

.section-body {
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
}
`;

content = content.replace('/* ═══ Section headers ═══ */', cssAdd + '\n/* ═══ Section headers ═══ */');

// Add the global actions button
content = content.replace('<template v-else>', '<template v-else>\n        <div class="global-actions">\n          <button type="button" class="secondary-btn" @click="openAllSections">Abrir Todos</button>\n          <button type="button" class="secondary-btn" @click="closeAllSections">Fechar Todos</button>\n        </div>');

// Now we define the sections to wrap
const sections = [
  { name: 'welcome', start: '1. WELCOME', end: '2. MESSAGE', header: 'Conteúdo do componente Info', resetBtn: 'handleResetWelcome' },
  { name: 'message', start: '2. MESSAGE', end: '3. PURPOSES', header: 'Conteúdo do componente Message', resetBtn: 'handleResetMessage' },
  { name: 'purposes', start: '3. PURPOSES', end: '4. PASTORAL TEAM', header: 'Propósitos', resetBtn: 'handleResetPurposes', hasAdd: 'addPurposeRow' },
  { name: 'pastoralTeam', start: '4. PASTORAL TEAM', end: '5. MINISTRIES', header: 'Equipa pastoral', resetBtn: 'handleResetPastoralTeam', hasAdd: 'addPastorRow' },
  { name: 'ministries', start: '5. MINISTRIES', end: '6. SERVICES', header: 'Ministérios', resetBtn: 'handleResetMinistriesPresentation', hasAdd: 'addMinistryRow' },
  { name: 'servicesBanner', start: '6. SERVICES BANNER', end: '7. LOCAL GATHERINGS CONTENT', header: 'Serviços Banner', resetBtn: 'handleResetServicesBanner' },
  { name: 'localGatherings', start: '7. LOCAL GATHERINGS CONTENT', end: '8. LOCAL GATHERING OPTIONS', header: 'Encontros Locais – Conteúdo', resetBtn: 'handleResetLocalGatherings' },
  { name: 'localGatheringOptions', start: '8. LOCAL GATHERING OPTIONS', end: '9. GALLERY', header: 'Pequenos Grupos', resetBtn: 'handleResetLocalGatheringOptions', hasAdd: 'addLocalGatheringOptionRow' },
  { name: 'gallery', start: '9. GALLERY', end: '10. SOCIAL MEDIA', header: 'Galeria', resetBtn: 'handleResetGallery', hasAdd: 'addGalleryImage' },
  { name: 'socialMedia', start: '10. SOCIAL MEDIA', end: '11. DONATIONS', header: 'Redes Sociais', resetBtn: 'handleResetSocialMedia', hasAdd: 'addSocialMediaRow' },
  { name: 'donations', start: '11. DONATIONS', end: '12. LOCATIONS', header: 'Contribuições', resetBtn: 'handleResetDonations' },
  { name: 'locations', start: '12. LOCATIONS', end: 'SAVE ROW', header: 'Localizações', resetBtn: 'handleResetLocations', hasAdd: 'addLocationRow' },
];

for (const sec of sections) {
  const startRegex = new RegExp(`(<!-- ════+[\\s\\S]*?${sec.start}[\\s\\S]*?════+ -->\\s*)<div class="(?:section-header|group-header)">`);
  const match = content.match(startRegex);
  if (!match) {
    console.error(`Could not find start for ${sec.name}`);
    continue;
  }
  
  // Find the end point
  const endRegex = new RegExp(`<!-- ════+[\\s\\S]*?${sec.end}[\\s\\S]*?════+ -->`);
  const endMatch = content.match(endRegex);
  if (!endMatch) {
    console.error(`Could not find end for ${sec.name}`);
    continue;
  }
  
  const blockStartIdx = match.index;
  const blockEndIdx = endMatch.index;
  
  let blockContent = content.substring(blockStartIdx, blockEndIdx);
  
  // Rewrite the block header
  let headerHtml = `
        <div class="section-container">
          <div class="section-header" @click="toggleSection('${sec.name}')">
            <div class="section-title">
              <i class="fa-solid fa-chevron-down" :class="{'rotate-180': openSections.${sec.name}}"></i>
              <span>${sec.header}</span>
            </div>
            <div class="actions">
              <button type="button" class="secondary-btn" @click.stop="${sec.resetBtn}">Reset</button>
              ${sec.hasAdd ? `<button type="button" @click.stop="${sec.hasAdd}">+ Adicionar${sec.name === 'locations' ? ' localização' : sec.name === 'gallery' ? ' foto' : ' linha'}</button>` : ''}
            </div>
          </div>
          <div v-show="openSections.${sec.name}" class="section-body">
  `;
  
  // Replace the old header with the new header
  blockContent = blockContent.replace(/<div class="(?:section-header|group-header)">[\s\S]*?<\/div>/, headerHtml.trim());
  
  // Close the section-body and section-container at the end of the block
  blockContent = blockContent.replace(/\s*$/, '\n          </div>\n        </div>\n\n        ');
  
  content = content.substring(0, blockStartIdx) + blockContent + content.substring(blockEndIdx);
}

fs.writeFileSync(file, content, 'utf-8');
console.log('Changes applied');
