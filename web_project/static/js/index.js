function showToast(idButton, idToast){
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(document.getElementById(idToast))
    document.getElementById(idButton).addEventListener('click', () => {
      toastBootstrap.show()
    })
}
showToast('newsletterBtn', 'liveToastNewsLetter');