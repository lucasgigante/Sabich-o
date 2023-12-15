

// script.js


function enviarParaPython() {
    var productName = document.getElementById("productName").value;

    // Verifica se o campo de texto está preenchido antes de mostrar o ícone
    if (productName.trim() !== '') {
        document.getElementById('enviarBtn').classList.remove('invisible');

        // Use AJAX para enviar o valor do input para o servidor Flask
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "{{ url_for('loading') }}", true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                // Manipule a resposta do servidor aqui, se necessário
                console.log(xhr.responseText);
            }
        };
        xhr.send(JSON.stringify({ productName: productName }));
    }



}


function reviewsScrape() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/results", true);  // Change to POST method
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
        }
    };
    xhr.send();
}



function resultScrape() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/results", true);  // Change to POST method
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
        }
    };
    xhr.send();
}


// Adicione um evento de clique ao ícone para acionar a função enviarParaPython
document.getElementById('enviarBtn').addEventListener('click', enviarParaPython);





function lerCSV(caminhoArquivo) {
    const reader = new FileReader();

    reader.onload = function (e) {
        const linhasDoCSV = e.target.result.split('\n');
        const cardsContainer = document.getElementById('content');

        for (let i = 1; i < linhasDoCSV.length; i++) {
            const colunas = linhasDoCSV[i].split(',');

            const card = document.createElement('div');
            card.classList.add('content');

            const centerDiv = document.createElement('div');
            centerDiv.classList.add('center-div');
            card.appendChild(centerDiv);

            const cardInner = document.createElement('div');
            cardInner.classList.add('card');
            centerDiv.appendChild(cardInner);

            const imagemContainer = document.createElement('div');
            imagemContainer.classList.add('imagem-container');
            cardInner.appendChild(imagemContainer);

            const textoPequeno = document.createElement('p');
            textoPequeno.classList.add('texto-pequeno');
            textoPequeno.textContent = colunas[3];
            imagemContainer.appendChild(textoPequeno);

            const imagem = document.createElement('img');
            imagem.classList.add('imagem-card');
            imagem.src = colunas[3];
            imagemContainer.appendChild(imagem);

            const textoContainer = document.createElement('div');
            textoContainer.classList.add('texto-container');
            cardInner.appendChild(textoContainer);

            const link = document.createElement('a');
            link.classList.add('link-card');
            link.href = colunas[3];
            textoContainer.appendChild(link);

            const containerDetalhes = document.createElement('div');
            containerDetalhes.classList.add('container-detalhes');
            textoContainer.appendChild(containerDetalhes);

            const formulario = document.createElement('form');
            formulario.method = 'post';
            formulario.action = '/search';
            containerDetalhes.appendChild(formulario);

            const verDetalhes = document.createElement('button');
            verDetalhes.classList.add('detalhes-botao');
            verDetalhes.textContent = 'Ver Detalhes';
            verDetalhes.addEventListener('click', function () {
                // Adicione a lógica para manipular o clique do botão aqui
                console.log('Clicou em Ver Detalhes para:', colunas[4]);
            });
            formulario.appendChild(verDetalhes);

            cardsContainer.appendChild(card);
        }
    };

    reader.readAsText(caminhoArquivo);
}


// Chame a função quando a página estiver carregada
document.addEventListener('DOMContentLoaded', function() {
    lerCSV('../data/search_page.csv');
});



