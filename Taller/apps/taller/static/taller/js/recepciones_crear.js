const input = document.getElementById('evidencias');
const cameraInput = document.getElementById('evidencias_camara');
const preview = document.getElementById('file-preview');
let previewUrls = [];

const collectFiles = () => {
  const files = [];
  if (input) {
    files.push(...Array.from(input.files));
  }
  if (cameraInput) {
    files.push(...Array.from(cameraInput.files));
  }
  return files;
};

const clearPreviewUrls = () => {
  previewUrls.forEach((url) => URL.revokeObjectURL(url));
  previewUrls = [];
};

const renderPreview = () => {
  if (!preview) {
    return;
  }

  clearPreviewUrls();
  preview.innerHTML = '';

  const files = collectFiles();
  if (files.length === 0) {
    preview.classList.add('hidden');
    return;
  }

  preview.classList.remove('hidden');

  files.forEach((file) => {
      const isImage = file.type.startsWith('image/');
      const li = document.createElement('li');
      li.className =
        'flex items-center gap-3 rounded-md border border-slate-200 px-3 py-2 text-sm text-slate-700';

      if (isImage) {
        const img = document.createElement('img');
        img.className = 'h-10 w-10 rounded object-cover flex-shrink-0';
        const previewUrl = URL.createObjectURL(file);
        previewUrls.push(previewUrl);
        img.src = previewUrl;
        li.appendChild(img);
      } else {
        // Icon for video
        li.innerHTML += `
          <span class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded bg-slate-100">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 002.25-2.25v-9A2.25 2.25 0 0013.5 6h-9A2.25 2.25 0 002.25 8.25v9A2.25 2.25 0 004.5 18.75z" />
            </svg>
          </span>`;
      }

      const info = document.createElement('div');
      info.className = 'flex flex-col min-w-0';
      info.innerHTML = `
        <span class="truncate font-medium">${file.name}</span>
        <span class="text-xs text-slate-400">${(file.size / 1024).toFixed(1)} KB</span>
      `;
      li.appendChild(info);
      preview.appendChild(li);
    });
};

if (input) {
  input.addEventListener('change', renderPreview);
}

if (cameraInput) {
  cameraInput.addEventListener('change', renderPreview);
}
