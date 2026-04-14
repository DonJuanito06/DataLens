document.getElementById('uploadBtn').addEventListener('click', async function () {
    const fileInput = document.getElementById('excelFile');
    const resultArea = document.getElementById('resultArea');
    const uploadBtn = this;

    // Validar archivo
    if (!fileInput.files || fileInput.files.length === 0) {
        alert("Por favor, selecciona un archivo Excel primero.");
        return;
    }

    const file = fileInput.files[0];
    const esEconomia = uploadBtn.classList.contains('btn-finance');
    const tipoAnalisis = esEconomia ? "financiero" : "poblacional";
    const color = esEconomia ? 'var(--green-mid)' : 'var(--blue-mid)';

    // Estado de carga
    resultArea.innerHTML = `
        <div class="loading-state">
            <div class="spinner" style="border-top-color: ${color}"></div>
            <p>Iniciando análisis <strong>${tipoAnalisis}</strong>…</p>
            <p style="font-size:0.8rem;opacity:0.6">Procesando datos con IA</p>
        </div>
    `;

    uploadBtn.disabled = true;
    const originalText = uploadBtn.innerText;
    uploadBtn.innerText = "Analizando…";

    const formData = new FormData();
    formData.append('file', file);
    formData.append('contexto', tipoAnalisis);

    try {
        const response = await fetch('http://127.0.0.1:5000/analizar', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            resultArea.innerHTML = `
                <div class="result-inner">
                    <h2>Reporte ${tipoAnalisis.charAt(0).toUpperCase() + tipoAnalisis.slice(1)}</h2>
                    <div class="content">${data.analysis}</div>
                </div>
            `;
        } else {
            resultArea.innerHTML = `
                <div class="result-inner">
                    <p style="color:#dc2626;font-size:0.9rem;">⚠ Error en el servidor: ${data.error}</p>
                </div>`;
        }

    } catch (error) {
        resultArea.innerHTML = `
            <div class="result-inner">
                <p style="color:#dc2626;font-weight:600;margin-bottom:0.5rem;">Error de conexión</p>
                <p style="font-size:0.875rem;color:var(--ink-muted)">No se pudo contactar con el servidor de Python.<br>
                Verifica que la terminal esté corriendo en <code style="background:#f3f4f6;padding:2px 6px;border-radius:4px;">http://127.0.0.1:5000</code></p>
            </div>`;
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.innerText = originalText;
    }
});
