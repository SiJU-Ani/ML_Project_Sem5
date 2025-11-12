(function () {
  const $ = (id) => document.getElementById(id);
  const out = (id, data) => { $(id).textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2); };
  let API_BASE = 'http://localhost:8000';
  let selectedFiles = [];

  // Configure PDF.js worker
  if (typeof pdfjsLib !== 'undefined') {
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
  }

  async function extractTextFromPDF(file) {
    const arrayBuffer = await file.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    let fullText = '';
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const textContent = await page.getTextContent();
      const pageText = textContent.items.map(item => item.str).join(' ');
      fullText += pageText + '\n';
    }
    return fullText;
  }

  function setBase(url) {
    if (!url) return;
    API_BASE = url.replace(/\/$/, '');
  }



  // Bulk Resume Processing
  $('pdfFiles').addEventListener('change', (e) => {
    selectedFiles = Array.from(e.target.files);
    const fileList = $('fileList');
    fileList.innerHTML = '';
    
    if (selectedFiles.length < 10 || selectedFiles.length > 20) {
      fileList.innerHTML = `<div style="color:#f88;padding:8px;">Please select between 10-20 PDF files (selected: ${selectedFiles.length})</div>`;
      $('processBulk').disabled = true;
      return;
    }

    selectedFiles.forEach((file, idx) => {
      const item = document.createElement('div');
      item.className = 'file-item';
      item.innerHTML = `
        <span class="name">${idx + 1}. ${file.name}</span>
        <button class="remove" data-idx="${idx}">Remove</button>
      `;
      fileList.appendChild(item);
    });

    fileList.querySelectorAll('.remove').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const idx = parseInt(e.target.dataset.idx);
        selectedFiles.splice(idx, 1);
        $('pdfFiles').value = '';
        $('pdfFiles').dispatchEvent(new Event('change'));
      });
    });

    $('processBulk').disabled = false;
  });

  $('processBulk').addEventListener('click', async () => {
    if (selectedFiles.length < 10 || selectedFiles.length > 20) {
      alert('Please select between 10-20 resume PDFs');
      return;
    }

    const jd = $('bulk_jd').value.trim();
    const skills = $('bulk_skills').value.split(/\n|,/).map(s => s.trim()).filter(Boolean);
    const exp = Number($('bulk_exp').value || 0);

    if (!jd) {
      alert('Please provide a job description');
      return;
    }

    const progressBar = $('bulkProgress');
    const resultsContainer = $('bulkResults');
    progressBar.className = 'progress-bar active';
    progressBar.innerHTML = '<div class="progress-fill" style="width:0%"></div>';
    resultsContainer.innerHTML = '<p style="color:#9fb2d1;">Extracting text from PDFs...</p>';
    $('processBulk').disabled = true;

    // Extract text from all PDFs first
    const items = [];
    for (let i = 0; i < selectedFiles.length; i++) {
      const file = selectedFiles[i];
      const progress = ((i + 1) / selectedFiles.length) * 50; // 50% for extraction
      progressBar.querySelector('.progress-fill').style.width = `${progress}%`;

      try {
        const resumeText = await extractTextFromPDF(file);
        items.push({
          fileName: file.name,
          resume_text: resumeText,
          job_description: jd,
          required_skills: skills
        });
      } catch (e) {
        items.push({
          fileName: file.name,
          resume_text: '',
          job_description: jd,
          required_skills: skills,
          error: String(e)
        });
      }
    }

    // Now call the batch endpoint with all resumes at once
    resultsContainer.innerHTML = '<p style="color:#9fb2d1;">Scoring candidates using AI...</p>';
    progressBar.querySelector('.progress-fill').style.width = '75%';

    let results = [];
    try {
      const res = await fetch(`${API_BASE}/api/v1/candidates/score/batch`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(items)
      });
      results = await res.json();
    } catch (e) {
      resultsContainer.innerHTML = `<p style="color:#f88;">Error: ${String(e)}</p>`;
      progressBar.className = 'progress-bar';
      $('processBulk').disabled = false;
      return;
    }

    progressBar.querySelector('.progress-fill').style.width = '100%';

    // Sort by score descending (already sorted by backend, but ensure)
    results.sort((a, b) => (b.overall_score || 0) - (a.overall_score || 0));
    const winner = results[0];

    // Calculate summary statistics
    const allScores = results.map(r => r.overall_score || 0);
    const avgScore = (allScores.reduce((a, b) => a + b, 0) / allScores.length).toFixed(1);
    const maxScore = Math.max(...allScores).toFixed(1);
    const minScore = Math.min(...allScores).toFixed(1);
    const topThree = results.slice(0, 3);

    // Display results
    let html = `
      <div class="stats-summary">
        <h3>📈 Screening Summary</h3>
        <div class="stats-grid">
          <div class="stat-box">
            <div class="stat-label">Total Candidates</div>
            <div class="stat-value">${results.length}</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Average Score</div>
            <div class="stat-value">${avgScore}</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Highest Score</div>
            <div class="stat-value">${maxScore}</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Lowest Score</div>
            <div class="stat-value">${minScore}</div>
          </div>
        </div>
      </div>

      <div class="winner-card">
        <h3>🏆 Top Candidate</h3>
        <div><strong>File:</strong> ${winner.fileName}</div>
        <div class="score-badge">Overall Score: ${(winner.overall_score || 0).toFixed(1)}/100</div>
        
        <div class="score-breakdown">
          <div class="score-item">
            <div class="label">SKILLS</div>
            <div class="value">${(winner.skills_score || 0).toFixed(1)}</div>
          </div>
          <div class="score-item">
            <div class="label">SEMANTIC</div>
            <div class="value">${(winner.semantic_score || 0).toFixed(1)}</div>
          </div>
        </div>

        ${winner.matched_skills && winner.matched_skills.length > 0 ? `
        <div class="skills-section">
          <h4>✅ Matched Skills (${winner.matched_skills.length})</h4>
          <div class="skill-tags">
            ${winner.matched_skills.map(s => `<span class="skill-tag matched">${s}</span>`).join('')}
          </div>
        </div>
        ` : ''}

        ${winner.missing_skills && winner.missing_skills.length > 0 ? `
        <div class="skills-section">
          <h4>❌ Missing Skills (${winner.missing_skills.length})</h4>
          <div class="skill-tags">
            ${winner.missing_skills.map(s => `<span class="skill-tag missing">${s}</span>`).join('')}
          </div>
        </div>
        ` : ''}

        <div class="remarks">
          <h4>💡 Why This is the Best Candidate:</h4>
          <ul>
            ${winner.explanation?.strengths?.map(s => `<li><strong>Strength:</strong> ${s}</li>`).join('') || '<li>No strengths data</li>'}
          </ul>
          ${winner.explanation?.gaps?.length ? `
            <h4 style="margin-top:12px;">Areas for Development:</h4>
            <ul>
              ${winner.explanation.gaps.map(g => `<li>${g}</li>`).join('')}
            </ul>
          ` : ''}
          <p><strong>Recommendation:</strong> ${winner.explanation?.recommendation || 'N/A'}</p>
        </div>
      </div>

      <div class="top-three">
        <h3>🥈 Top 3 Candidates</h3>
        <div class="cards-row">
          ${topThree.map((r, idx) => `
            <div class="candidate-card rank-${idx + 1}">
              <div class="rank-badge">#${idx + 1}</div>
              <div class="candidate-name">${r.fileName}</div>
              <div class="candidate-score">${(r.overall_score || 0).toFixed(1)}</div>
              <div class="score-breakdown-small">
                <div><small>Skills: ${(r.skills_score || 0).toFixed(1)}</small></div>
                <div><small>Semantic: ${(r.semantic_score || 0).toFixed(1)}</small></div>
              </div>
            </div>
          `).join('')}
        </div>
      </div>

      <div class="all-results">
        <h4>📊 All Candidates Ranked</h4>
        <table class="results-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>File Name</th>
              <th>Overall Score</th>
              <th>Skills</th>
              <th>Semantic</th>
              <th>Matched Skills</th>
            </tr>
          </thead>
          <tbody>
            ${results.map((r, idx) => `
              <tr class="${idx === 0 ? 'rank-1' : ''}">
                <td><strong>${idx + 1}</strong></td>
                <td>${r.fileName}</td>
                <td><strong>${(r.overall_score || 0).toFixed(1)}</strong></td>
                <td>${(r.skills_score || 0).toFixed(1)}</td>
                <td>${(r.semantic_score || 0).toFixed(1)}</td>
                <td>${r.matched_skills ? r.matched_skills.length : 0}/${r.matched_skills ? r.matched_skills.length + (r.missing_skills ? r.missing_skills.length : 0) : 0}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `;

    resultsContainer.innerHTML = html;
    progressBar.className = 'progress-bar';
    $('processBulk').disabled = false;
  });

  // init - no longer needed
})();
