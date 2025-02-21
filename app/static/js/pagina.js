//Trocando a cor de "Essence"

let tamanho = 1;
      let cores = ['brown', 'purple', 'orange'];
      let corAtual = 0;

      function mudarEstilo() {

         // Muda a cor da fonte
         corAtual = (corAtual + 1) % cores.length;

         // Aplica as mudanças
         const h1 = document.getElementById('boasVindas');
         h1.style.color = cores[corAtual];
      }




      function showNotification(message) {
        // Cria um novo elemento para a notificação
        let notification = document.createElement("div");
        notification.className = "notification";
        notification.innerText = message;
    
        // Adiciona ao container de notificações
        document.getElementById("notification-container").appendChild(notification);
    
        // Remove a notificação após 5 segundos
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
    
    // WebSocket para notificações
    const ws = new WebSocket("ws://" + window.location.host + "/ws");
    
    ws.onmessage = function(event) {
        showNotification(event.data); // Agora as mensagens aparecem bonitinhas
    };
    
    function enviarClique(nomePerfume) {
        ws.send(nomePerfume);
    }
    