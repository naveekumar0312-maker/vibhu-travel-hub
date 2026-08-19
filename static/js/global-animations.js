/**
 * GLOBAL VEHICLE WHATSAPP BOOKING FLOW & ANIMATIONS
 * Vibhu Travel Hub
 */

window.openVehicleWhatsApp = function (vehicleName, vehicleCapacity) {
    const name = (vehicleName || 'Vehicle').trim();
    let capacity = (vehicleCapacity || '').trim();

    if (capacity && !capacity.toLowerCase().includes('seater')) {
        capacity = `${capacity} Seater`;
    }
    if (!capacity) {
        capacity = 'Standard Seating';
    }

    const message = `Hello Vibhu Travel Hub,\n\nI would like to book the following vehicle:\n\nVehicle: ${name}\nSeating Capacity: ${capacity}\n\nThank you.`;

    const encodedMessage = encodeURIComponent(message);
    const whatsappUrl = `https://wa.me/919655866660?text=${encodedMessage}`;
    window.open(whatsappUrl, '_blank');
};

document.addEventListener('DOMContentLoaded', () => {
    // Global Event Delegation for Vehicle Booking Buttons
    document.body.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-vehicle-name], .btn-book-vehicle');
        if (btn) {
            e.preventDefault();
            e.stopPropagation();
            const vName = btn.getAttribute('data-vehicle-name');
            const vCap = btn.getAttribute('data-vehicle-capacity');
            window.openVehicleWhatsApp(vName, vCap);
        }
    });
});
