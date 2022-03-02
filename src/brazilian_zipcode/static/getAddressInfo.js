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
    const externalDiv = document.createElement("div");
    externalDiv.classList.add("form-row");
    externalDiv.setAttribute("meta-id", label)


    const innerDiv = document.createElement("div");
    innerDiv.classList.add("input-field");

    const valueDiv = document.createElement("div");
    const labelDiv = document.createElement("div");
    labelDiv.classList.add("readonly-label");

    const labelElement = document.createElement("label");
    labelElement.innerText = label + ":";
    innerDiv.appendChild(labelElement);

    valueDiv.classList.add("readonly");
    valueDiv.innerText = value;
    innerDiv.appendChild(valueDiv);

    externalDiv.appendChild(innerDiv)
    parentDiv.appendChild(externalDiv);
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
    const input = document.querySelector(zipcodeSelector);
    input.addEventListener("focusout", handleOnFocusOutEvent)
});