document.addEventListener("DOMContentLoaded", function () {
    const fireSound = document.getElementById("fireSound");

    if (window.playSound && fireSound) {
        fireSound.play().catch(function (e) {
            console.log("Autoplay prevented:", e);
        });
    }
});

function stopAlarm() {
    const fireSound = document.getElementById("fireSound");
    if (fireSound) {
        fireSound.pause();
        fireSound.currentTime = 0;
    }
}
