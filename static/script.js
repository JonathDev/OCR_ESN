function showVerso(element) {
    var carte = element.closest('.carte');
    carte.classList.add('flipped');
}

function showRecto(element) {
    var carte = element.closest('.carte');
    carte.classList.remove('flipped');
}