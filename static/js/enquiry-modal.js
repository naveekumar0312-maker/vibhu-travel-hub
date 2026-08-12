document.addEventListener('DOMContentLoaded', function () {
    const modalElement = document.getElementById('enquiryModal');
    if (!modalElement) {
        console.error('Enquiry Modal not found.');
        return;
    }

    const form = document.getElementById('enquiryForm');
    const alertBox = document.getElementById('enquiryAlertBox');
    const submitBtn = document.getElementById('enquiryBtnSubmit');

    // Auto-populate data when opened by Book Now buttons
    modalElement.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        
        if (button) {
            const destValue = button.getAttribute('data-destination');
            const placeValue = button.getAttribute('data-place') || button.getAttribute('data-city');
            
            const hiddenDest = document.getElementById('hiddenStateDest');
            const hiddenPlace = document.getElementById('hiddenTouristPlace');
            
            if (hiddenDest && destValue) {
                hiddenDest.value = destValue;
            }
            if (hiddenPlace && placeValue) {
                hiddenPlace.value = placeValue;
            }
        }
    });

    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }

            // Show loading state safely
            if (submitBtn) {
                const btnText = submitBtn.querySelector('.btn-text');
                const btnSpinner = submitBtn.querySelector('.btn-spinner');
                
                submitBtn.disabled = true;
                if (btnText) btnText.style.display = 'none';
                if (btnSpinner) btnSpinner.classList.remove('d-none');
            }
            
            if (alertBox) {
                alertBox.style.display = 'none';
                alertBox.className = 'enquiry-alert';
            }

            const formData = new FormData(form);

            fetch('/api/enquiry/submit/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success' || data.success) {
                    if (alertBox) {
                        alertBox.textContent = data.message || "Enquiry saved successfully. Redirecting to WhatsApp...";
                        alertBox.className = "enquiry-alert success";
                        alertBox.style.display = 'block';
                    }
                    
                    // Build WhatsApp Message
                    const waText = data.wa_text || "Hello Vibhu Travel Hub, I would like to book a trip.";
                    
                    const waNumber = "919655866660";
                    const waUrl = `https://wa.me/${waNumber}?text=${encodeURIComponent(waText)}`;

                    // Redirect to WhatsApp after short delay
                    setTimeout(() => {
                        window.open(waUrl, '_blank');
                        form.reset();
                        // Hide modal safely using Bootstrap instance
                        if (typeof bootstrap !== 'undefined') {
                            const modalInstance = bootstrap.Modal.getInstance(modalElement);
                            if (modalInstance) {
                                modalInstance.hide();
                            }
                        }
                        if (alertBox) alertBox.style.display = 'none';
                    }, 1500);
                    
                } else {
                    if (alertBox) {
                        alertBox.textContent = data.message || "Something went wrong. Please try again.";
                        alertBox.className = "enquiry-alert error";
                        alertBox.style.display = 'block';
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (alertBox) {
                    alertBox.textContent = "Network error. Please try again later.";
                    alertBox.className = "enquiry-alert error";
                    alertBox.style.display = 'block';
                }
            })
            .finally(() => {
                // Restore button state safely
                if (submitBtn) {
                    submitBtn.disabled = false;
                    const btnText = submitBtn.querySelector('.btn-text');
                    const btnSpinner = submitBtn.querySelector('.btn-spinner');
                    if (btnText) btnText.style.display = 'block';
                    if (btnSpinner) btnSpinner.classList.add('d-none');
                }
            });
        });
    }
});
