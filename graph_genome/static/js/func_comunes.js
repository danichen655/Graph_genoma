$(document).ready(function() {
    const input1 = $("#loadFasta");
    const input2 = $("#loadMetadata");
    const input3 = $("#loadGraphGenome");
    const label1 = $("#labelFasta");
    const label2 = $("#labelMetadata");
    const label3 = $("#labelGraphGenome");
    const btnSubmit = $("#submit");

    // Al cargar un fasta, habilitar los botones que se pueden usar
    input1.on("change", function() {
        input2.prop("disabled", false);
        label2.removeClass("disabled");
        input3.prop("disabled", true);
        label3.addClass("disabled");
        btnSubmit.prop("disabled", false);
        btnSubmit.removeClass("disabled");
    });
    // Al cargar un graph genome, habilitar los botones que se pueden usar
    input3.on("change", function() {
        input1.prop("disabled", true);
        label1.addClass("disabled");
        input2.prop("disabled", false);
        label2.removeClass("disabled");
        btnSubmit.prop("disabled", false);
        btnSubmit.removeClass("disabled");
    });
});

function openInfo() {
    $("#myModal").css("display", "block"); // Mostrar info
}
function closeModal() {
    $("#myModal").css("display", "none"); // Cerrar info
}

// Deshabilitar todos los botones para que no haya problemas al hacer click en submit
function disableAllBtn(){
    submit.disabled = false;
    submit.classList.add("disabled");
    loadFasta.disabled = false;
    labelFasta.classList.add("disabled");
    loadMetadata.disabled = false;
    labelMetadata.classList.add("disabled");
    loadGraphGenome.disabled = false;
    labelGraphGenome.classList.add("disabled");
}