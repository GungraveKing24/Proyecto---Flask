let sidebar = document.querySelector(".sidebar");
  let closeBtn = document.querySelector("#btn");
  let searchBtn = document.querySelector(".bx-search");
  closeBtn.addEventListener("click", () => {
    sidebar.classList.toggle("open");
    menuBtnChange(); // Llama a la función para cambiar el botón de menú
    hideSectionIfSmallScreen(); // Comprueba si la pantalla es pequeña y oculta la sección si es necesario
  });
  searchBtn.addEventListener("click", ()=>{ // Sidebar open when you click on the search iocn
    sidebar.classList.toggle("open");
    menuBtnChange(); //calling the function(optional)
    hideSectionIfSmallScreen();
  });
  // following are the code to change sidebar button(optional)
  function menuBtnChange() {
    if (sidebar.classList.contains("open")) {
      closeBtn.classList.replace("bx-menu", "bx-menu-alt-right"); // replacing the icon's class
      closeBtn.style.color = ""; // Resetting the button color when the sidebar is closed
    } else {
      closeBtn.classList.replace("bx-menu-alt-right", "bx-menu"); // replacing the icon's class
      closeBtn.style.color = "transparent";
      hideSectionIfSmallScreen();
    }
  }

  function hideSectionIfSmallScreen() {
    // Obtener el ancho actual de la ventana del navegador
    const windowWidth = window.innerWidth;

    // Si el ancho de la ventana es menor que 321px y la barra lateral está abierta, oculta la sección
    if (windowWidth < 375 && sidebar.classList.contains("open")) {
      const homeSection = document.querySelector(".home-section");
      if (homeSection) {
        homeSection.style.display = "none";
      }
    } else {
      // Si el ancho de la ventana es mayor o igual a 321px, o la barra lateral está cerrada, muestra la sección
      const homeSection = document.querySelector(".home-section");
      if (homeSection) {
        homeSection.style.display = ""; // O el valor apropiado según el diseño
      }
    }
  }