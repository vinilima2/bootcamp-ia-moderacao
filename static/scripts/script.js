function alterarModalPost() {
    document.querySelector('.modal-post').classList.toggle('is-active')
}

function alterarModalResposta() {
    document.querySelector('.modal-resposta').classList.toggle('is-active')
}

document.getElementById('botao-novo-post').addEventListener('click', () => alterarModalPost())
document.getElementById('cancelar-post').addEventListener('click', () => alterarModalPost())
document.getElementById('cancelar-resposta').addEventListener('click', () => alterarModalResposta())

document.querySelectorAll('.comentario').forEach(element => {
    element.addEventListener('click',
        (event) => {
            let postID = element.attributes.getNamedItem('post-id').value
            document.getElementById('post_id').value = postID
            alterarModalResposta()
        })
})

document.getElementById('botao-menu').addEventListener('click', () => {
    document.getElementById('menu').classList.toggle('is-hidden')
})