const Form = document.querySelector('#form')
const error = document.querySelector('#alert')

if (Form) {
    Form.addEventListener('submit', (event) => {
        let message = []
        let Contact = Form.elements.contact.value;
        let Name = Form.elements.name.value;
        for (i = 0; i < Name.length; i++) {
            if ((Name.charCodeAt(i) < 65 || Name.charCodeAt(i) > 91) && (Name.charCodeAt(i) < 97  || Name.charCodeAt(i) > 123) && Name.charCodeAt(i) != 32) {
                message.push('Invalid Name');
                console.log(Name.charCodeAt(i), Name[i]);
                break;
            }
        }
        let contactIsNumber = true

        for (i = 0; i < Contact.length; i++) {
            let num = parseInt(Contact[i])

            if (!(num >= 0 && num <= 9)) {
                contactIsNumber = false
                break;
            }
            console.log(num);
        }

        let Age = Form.elements.age.value;

        if (!((contactIsNumber && Contact.length === 10) || (Contact.length===0))) {
            message.push('Invalid Contact')
        }

        else if (parseInt(Age) <= 0 || parseInt(Age) >= 100) {
            message.push('Invalid Age')
        }
        if (message.length > 0) {
            event.preventDefault()
            error.classList.add('Alert')
            error.innerText = message.join(', ')
        }
        else {
            error.classList.remove('Alert')
            error.innerText = ''
        }
    })
}
