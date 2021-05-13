const Form = document.querySelector('#form')
const error = document.querySelector('#alert')


if (Form) {
    Form.addEventListener('submit', (event) => {
        let message = []
        let Quiz_1 = (Form.elements.quiz1.value);
        let Quiz_2 = (Form.elements.quiz2.value);
        let Mid_Sem = (Form.elements.mst.value);
        let End_Sem = (Form.elements.est.value);

        if (parseInt(Quiz_1) < 0 || parseInt(Quiz_1) >= 11) {
            message.push("Quiz 1 marks aren't between 0 and 10")
        }
        else if(parseInt(Quiz_2) < 0 || parseInt(Quiz_2) >= 11){
            // console.log(Quiz_2)
            message.push("Quiz 2 marks aren't between 0 and 10")
        }
        else if(parseInt(Mid_Sem) < 0 || parseInt(Mid_Sem) >= 31){
            // console.log(Mid_Sem)
            message.push("Mid Sem marks aren't between 0 and 30")
        }
        else if(parseInt(End_Sem) < 0 || parseInt(End_Sem) >= 51){
            // console.log(End_Sem)
            message.push("End Sem marks aren't between 0 and 50")
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
        console.log("hello")
    })
}
