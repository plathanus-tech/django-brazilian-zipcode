const zipcodeSelector = "[meta_id='meta_zipcode_info']";
const saveButtonSelector = "[name='_save']"

function isNumeric(str) {
    if (typeof str != "string") return false
    return !isNaN(str) && 
           !isNaN(parseFloat(str))
  }

function onlyDigits(value) {
    return value.replace(/\D/g, "")
};

function removeReadOnlyInput(label) {
    const previousElement = document.querySelector(`[meta-id='${label}']`);
    if (previousElement !== null) {
        previousElement.remove();
    }
}

function createReadOnlyInput(label, value) {
    const input = document.querySelector(zipcodeSelector);
    const parentDiv = input.parentNode.parentNode.parentNode;
    
    removeReadOnlyInput(label);
    const div = document.createElement("div");
    div.classList.add("form-row");
    div.setAttribute("meta-id", label)

    const valueDiv = document.createElement("div");
    const labelElement = document.createElement("label");

    labelElement.innerText = label + ":";
    labelElement.classList.add("required");
    div.appendChild(labelElement);

    valueDiv.classList.add("readonly");
    valueDiv.innerText = value;
    div.appendChild(valueDiv);

    parentDiv.appendChild(div);
}

function getAddressInfo(zipcode) {
    const saveButton = document.querySelector(saveButtonSelector);

    fetch(`/api/address_info?zipcode=${zipcode}`).then((response) => {
        if (response.status !== 200) {
            saveButton.setAttribute('disabled', true)
            removeReadOnlyInput("Rua");
            removeReadOnlyInput("Bairro");
            removeReadOnlyInput("Cidade");
            removeReadOnlyInput("UF");
            window.alert("CEP não encontrado ou serviço indisponível");
            return
        }
        response.json().then(data => {
            createReadOnlyInput("Rua", data.street);
            createReadOnlyInput("Bairro", data.district);
            createReadOnlyInput("Cidade", data.city);
            createReadOnlyInput("UF", data.state_initials);
        })
    })
    saveButton.removeAttribute('disabled');
};

function handleOnFocusOutEvent(event) {
    var zipcode = event.target.value;
    zipcode = onlyDigits(zipcode);
    
    const input = document.querySelector(zipcodeSelector);
    input.value = zipcode;

    if (zipcode.length !== 8) {
        return;
    }
    if (!isNumeric(zipcode)) {
        return
    }
    getAddressInfo(zipcode);
};



$(document).ready(function () {
    const input = document.querySelector(zipcodeMetaId);
    input.addEventListener("focusout", handleOnFocusOutEvent)
});