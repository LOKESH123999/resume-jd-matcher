// Resume-Job Description Matcher - Frontend JavaScript

// Global variables
let currentAnalysis = null;
let analysisHistory = [];

// API Configuration
const API_BASE_URL = window.location.origin === 'http://localhost:3000' 
    ? 'http://localhost:8000' 
    : window.location.origin;

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize event listeners
    document.getElementById('analysisForm').addEventListener('submit', handleAnalysisSubmit);
    
    // Load analysis history
    loadAnalysisHistory();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Smooth scrolling for navigation links
    initializeSmoothScrolling();
    
    console.log('Resume Matcher App initialized');
}

// Handle form submission
async function handleAnalysisSubmit(event) {
    event.preventDefault();
    
    const resumeText = document.getElementById('resumeText').value.trim();
    const jobText = document.getElementById('jobText').value.trim();
    
    // Validate inputs
    if (!validateInputs(resumeText, jobText)) {
        return;
    }
    
    // Show loading modal
    showLoadingModal();
    
    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/api/v1/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                resume_text: resumeText,
                job_description: jobText
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Analysis failed');
        }
        
        const result = await response.json();
        currentAnalysis = result;
        
        // Hide loading modal
        hideLoadingModal();
        
        // Display results
        displayResults(result);
        
        // Scroll to results
        scrollToResults();
        
        // Refresh history
        setTimeout(() => loadAnalysisHistory(), 1000);
        
    } catch (error) {
        hideLoadingModal();
        showError('Analysis failed: ' + error.message);
        console.error('Analysis error:', error);
    }
}

// Validate input texts
function validateInputs(resumeText, jobText) {
    if (resumeText.length < 50) {
        showError('Resume text must be at least 50 characters long');
        return false;
    }
    
    if (jobText.length < 50) {
        showError('Job description must be at least 50 characters long');
        return false;
    }
    
    return true;
}

// Display analysis results
function displayResults(result) {
    if (!result.success) {
        showError('Analysis failed: ' + (result.error || 'Unknown error'));
        return;
    }
    
    const { score_breakdown, skills, ai_feedback } = result;
    
    // Update score overview
    updateScoreOverview(score_breakdown, skills);
    
    // Update skills lists
    updateSkillsLists(skills);
    
    // Update AI feedback
    updateAIFeedback(ai_feedback);
    
    // Show results section
    document.getElementById('results').style.display = 'block';
    
    // Add animation
    document.getElementById('results').classList.add('fade-in');
}

// Update score overview section
function updateScoreOverview(scoreBreakdown, skills) {
    // Overall score
    const overallScore = document.getElementById('overallScore');
    overallScore.textContent = scoreBreakdown.score.toFixed(1) + '%';
    
    // Score category
    const scoreCategory = document.getElementById('scoreCategory');
    scoreCategory.textContent = scoreBreakdown.category;
    scoreCategory.className = 'score-category ' + scoreBreakdown.category;
    
    // Similarity score
    document.getElementById('similarityScore').textContent = scoreBreakdown.similarity_score.toFixed(1) + '%';
    
    // Skill score
    document.getElementById('skillScore').textContent = scoreBreakdown.skill_match_score.toFixed(1) + '%';
    
    // Skill ratio
    const matchedCount = skills.matched_skills.length;
    const totalCount = skills.matched_skills.length + skills.missing_skills.length;
    document.getElementById('skillRatio').textContent = `${matchedCount}/${totalCount} skills`;
    
    // Total skills
    document.getElementById('totalSkills').textContent = totalCount;
}

// Update skills lists
function updateSkillsLists(skills) {
    // Matched skills
    const matchedSkillsDiv = document.getElementById('matchedSkills');
    if (skills.matched_skills.length > 0) {
        matchedSkillsDiv.innerHTML = skills.matched_skills
            .map(skill => `<span class="skill-badge matched">${skill}</span>`)
            .join('');
    } else {
        matchedSkillsDiv.innerHTML = '<p class="text-muted">No matched skills found</p>';
    }
    
    // Missing skills
    const missingSkillsDiv = document.getElementById('missingSkills');
    if (skills.missing_skills.length > 0) {
        missingSkillsDiv.innerHTML = skills.missing_skills
            .map(skill => `<span class="skill-badge missing">${skill}</span>`)
            .join('');
    } else {
        missingSkillsDiv.innerHTML = '<p class="text-muted">No missing skills found</p>';
    }
}

// Update AI feedback section
function updateAIFeedback(aiFeedback) {
    // Fit analysis
    document.getElementById('fitAnalysis').textContent = aiFeedback.fit_analysis || 'Analysis not available';
    
    // Skills to learn
    const skillsToLearnDiv = document.getElementById('skillsToLearn');
    if (aiFeedback.skills_to_learn && aiFeedback.skills_to_learn.length > 0) {
        skillsToLearnDiv.innerHTML = aiFeedback.skills_to_learn
            .map(skill => `
                <div class="skill-item">
                    <div class="skill-name">${skill.skill || 'Unknown Skill'}</div>
                    <div class="skill-importance">${skill.importance || 'Importance not specified'}</div>
                </div>
            `).join('');
    } else {
        skillsToLearnDiv.innerHTML = '<p class="text-muted">No skill recommendations available</p>';
    }
    
    // Learning resources
    const resourcesDiv = document.getElementById('learningResources');
    if (aiFeedback.learning_resources && aiFeedback.learning_resources.length > 0) {
        resourcesDiv.innerHTML = aiFeedback.learning_resources
            .map(resource => `
                <div class="resource-item">
                    <div class="resource-skill">${resource.skill || 'Unknown Skill'}</div>
                    <div class="resource-course">${resource.course || 'Course not specified'}</div>
                    <div class="resource-platform">${resource.platform || 'Platform not specified'}</div>
                    ${resource.link ? `<div><a href="${resource.link}" target="_blank" class="resource-link">View Course →</a></div>` : ''}
                </div>
            `).join('');
    } else {
        resourcesDiv.innerHTML = '<p class="text-muted">No learning resources available</p>';
    }
    
    // Improvement tip
    document.getElementById('improvementTip').textContent = aiFeedback.improvement_tip || 'No improvement tip available';
}

// Load analysis history
async function loadAnalysisHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/analyses?limit=10`);
        
        if (!response.ok) {
            throw new Error('Failed to load history');
        }
        
        const analyses = await response.json();
        displayAnalysisHistory(analyses);
        
    } catch (error) {
        console.error('Error loading history:', error);
        document.getElementById('historyContent').innerHTML = `
            <div class="text-center py-4">
                <i class="bi bi-exclamation-triangle text-warning display-4"></i>
                <p class="mt-3">Unable to load analysis history</p>
            </div>
        `;
    }
}

// Display analysis history
function displayAnalysisHistory(analyses) {
    const historyContent = document.getElementById('historyContent');
    
    if (analyses.length === 0) {
        historyContent.innerHTML = `
            <div class="text-center py-4">
                <i class="bi bi-inbox text-muted display-4"></i>
                <p class="mt-3">No analysis history available</p>
                <p class="text-muted">Start by analyzing your first resume!</p>
            </div>
        `;
        return;
    }
    
    historyContent.innerHTML = analyses
        .map(analysis => {
            const date = new Date(analysis.created_at).toLocaleDateString();
            const preview = analysis.job_description.substring(0, 100) + '...';
            
            return `
                <div class="history-item">
                    <div class="history-date">
                        <i class="bi bi-calendar me-2"></i>${date}
                    </div>
                    <div class="history-score">
                        <i class="bi bi-graph-up me-2"></i>
                        Score: ${analysis.fit_score.toFixed(1)}% (${analysis.fit_category})
                    </div>
                    <div class="history-preview">${preview}</div>
                    <div class="mt-2">
                        <button class="btn btn-sm btn-outline-primary" onclick="viewAnalysis(${analysis.id})">
                            <i class="bi bi-eye me-1"></i>View Details
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteAnalysis(${analysis.id})">
                            <i class="bi bi-trash me-1"></i>Delete
                        </button>
                    </div>
                </div>
            `;
        })
        .join('');
}

// View specific analysis
async function viewAnalysis(analysisId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/analyses/${analysisId}`);
        
        if (!response.ok) {
            throw new Error('Failed to load analysis');
        }
        
        const analysis = await response.json();
        
        // Convert to display format
        const displayResult = {
            success: true,
            score_breakdown: {
                score: analysis.fit_score,
                category: analysis.fit_category,
                similarity_score: analysis.similarity_score,
                skill_match_score: analysis.skill_match_score
            },
            skills: {
                matched_skills: analysis.matched_skills,
                missing_skills: analysis.missing_skills,
                skill_match_score: analysis.skill_match_score
            },
            ai_feedback: analysis.ai_feedback
        };
        
        // Display results
        displayResults(displayResult);
        
        // Scroll to results
        scrollToResults();
        
    } catch (error) {
        showError('Failed to load analysis: ' + error.message);
    }
}

// Delete analysis
async function deleteAnalysis(analysisId) {
    if (!confirm('Are you sure you want to delete this analysis?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/analyses/${analysisId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete analysis');
        }
        
        // Refresh history
        loadAnalysisHistory();
        
        showSuccess('Analysis deleted successfully');
        
    } catch (error) {
        showError('Failed to delete analysis: ' + error.message);
    }
}

// Show loading modal
function showLoadingModal() {
    const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
    modal.show();
}

// Hide loading modal
function hideLoadingModal() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
    if (modal) {
        modal.hide();
    }
}

// Scroll to results section
function scrollToResults() {
    document.getElementById('results').scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
    });
}

// Show error message
function showError(message) {
    // Create toast alert
    const toastHtml = `
        <div class="toast align-items-center text-white bg-danger border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi bi-exclamation-triangle me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    showToast(toastHtml);
}

// Show success message
function showSuccess(message) {
    const toastHtml = `
        <div class="toast align-items-center text-white bg-success border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi bi-check-circle me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    showToast(toastHtml);
}

// Show toast notification
function showToast(html) {
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toastContainer';
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    // Add toast to container
    toastContainer.insertAdjacentHTML('beforeend', html);
    
    // Initialize and show toast
    const toastElement = toastContainer.lastElementChild;
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

// Initialize tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize smooth scrolling
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Utility function to format text
function formatText(text, maxLength = 100) {
    if (text.length <= maxLength) {
        return text;
    }
    return text.substring(0, maxLength) + '...';
}

// Utility function to get score color
function getScoreColor(score) {
    if (score >= 75) {
        return '#28a745'; // Green
    } else if (score >= 50) {
        return '#ffc107'; // Yellow
    } else {
        return '#dc3545'; // Red
    }
}

// Utility function to format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Export functions for global access
window.viewAnalysis = viewAnalysis;
window.deleteAnalysis = deleteAnalysis;
