document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("premiumEnquiryForm");
    const alertBox = document.getElementById("premiumAlertBox");
    const submitBtn = document.getElementById("premiumBtnSubmit");
    const enquiryModal = document.getElementById('premiumEnquiryModal');

    if (enquiryModal) {
        enquiryModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const vehicleSelect = document.getElementById('premiumVehicle');
            const passengerInput = document.getElementById('premiumPassengers');
            
            if (button) {
                const vehicleName = button.getAttribute('data-vehicle-name');
                const vehicleSeats = button.getAttribute('data-vehicle-seats');
                
                if (vehicleName) {
                    // Pre-fill and lock
                    if (vehicleSelect) {
                        let optionExists = false;
                        for (let i = 0; i < vehicleSelect.options.length; i++) {
                            if (vehicleSelect.options[i].value === vehicleName) {
                                optionExists = true;
                                break;
                            }
                        }
                        if (!optionExists) {
                            vehicleSelect.add(new Option(vehicleName, vehicleName));
                        }
                        vehicleSelect.value = vehicleName;
                        vehicleSelect.style.pointerEvents = 'none';
                        vehicleSelect.style.background = '#e9ecef';
                    }
                    if (passengerInput && vehicleSeats) {
                        passengerInput.value = vehicleSeats;
                        passengerInput.readOnly = true;
                        passengerInput.style.background = '#e9ecef';
                    }
                } else {
                    // Unlock for generic button
                    if (vehicleSelect) {
                        vehicleSelect.value = '';
                        vehicleSelect.style.pointerEvents = 'auto';
                        vehicleSelect.style.background = '';
                    }
                    if (passengerInput) {
                        passengerInput.value = '';
                        passengerInput.readOnly = false;
                        passengerInput.style.background = '';
                    }
                }
            }
        });
    }

    if (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();

            // Validate fields
            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }

            // Show loading state
            const btnText = submitBtn.querySelector(".btn-text");
            const btnSpinner = submitBtn.querySelector(".btn-spinner");
            
            submitBtn.disabled = true;
            if (btnText) btnText.style.display = "none";
            if (btnSpinner) btnSpinner.classList.remove("d-none");
            
            alertBox.style.display = "none";
            alertBox.className = "";

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
                    alertBox.textContent = "Thank you! Our team will contact you shortly.";
                    alertBox.className = "success";
                    form.reset();
                    
                    // Close modal after 3 seconds
                    setTimeout(() => {
                        const modalEl = document.getElementById('premiumEnquiryModal');
                        const modalInstance = bootstrap.Modal.getInstance(modalEl);
                        if (modalInstance) {
                            modalInstance.hide();
                        }
                        alertBox.style.display = "none";
                    }, 3000);
                } else {
                    alertBox.textContent = data.message || "Something went wrong. Please try again.";
                    alertBox.className = "error";
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alertBox.textContent = "Network error. Please try again later.";
                alertBox.className = "error";
            })
            .finally(() => {
                submitBtn.disabled = false;
                if (btnText) btnText.style.display = "block";
                if (btnSpinner) btnSpinner.classList.add("d-none");
                alertBox.style.display = "block";
            });
        });
    }
});
