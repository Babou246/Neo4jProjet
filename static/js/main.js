/*=============== SHOW MODAL ===============*/
const showModal = (openButton, modalContent) =>{
    const openBtn = document.getElementById(openButton),
    modalContainer = document.getElementById(modalContent)
    
    if(openBtn && modalContainer){
        openBtn.addEventListener('click', ()=>{
            modalContainer.classList.add('show-modal')
        })
    }
}
showModal('open-modal','modal-container')

/*=============== CLOSE MODAL ===============*/
const closeBtn = document.querySelectorAll('.close-modal')

function closeModal(){
    const modalContainer = document.getElementById('modal-container')
    modalContainer.classList.remove('show-modal')
}
closeBtn.forEach(c => c.addEventListener('click', closeModal))

// POPUP AJOUT PAR L'ADMINISTRATEUR DU SITE
const Fermer = document.getElementById('fermer')
const Ajouter = document.getElementById('ajouter')
const Add_user = document.querySelector('.add_user')
const Update = document.querySelector('.add_users')
const Modif = document.querySelectorAll('.modif')
const Archive = document.querySelectorAll('.archive')
const li = document.querySelectorAll('li')
const note = document.querySelector('.notification')
const rechercheImg = document.getElementById('rechercheImg')
const formSearch = document.getElementById('formSearch')
const rechercherInput =  document.querySelector('.rechercherInput')


Modif.forEach(modif=>modif.addEventListener('click',()=>{Update.style.display='flex'}))
Ajouter.addEventListener('click',()=>{Add_user.style.display='flex'})
Fermer.addEventListener('click',()=>{Add_user.style.display='none'})
rechercheImg.addEventListener('click',()=>{rechercherInput.style.display='flex'})

// LA PARTIE RECHERCHE VIA LA FORMULAIRE DE RECHERCHE

const userCardTemplate = document.querySelector("[data-user-template]")
// const userCardContainer = document.querySelector("[data-user-cards-container]")
// const searchInput = document.querySelector("[data-search]")

// let users = []

// searchInput.addEventListener("input", e => {
//   const value = e.target.value.toLowerCase()
//   users.forEach(user => {
//     const isVisible =
//       user.name.toLowerCase().includes(value) ||
//       user.email.toLowerCase().includes(value)
//     user.element.classList.toggle("hide", !isVisible)
//   })
// })

fetch("https://127.0.0.1:5000/listes")
  .then(res => res.json())
  .then(data => {console.log(data)})