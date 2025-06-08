// ../script/login.js

// ------------------ Seleção de Elementos do DOM ------------------
const loginForm = document.getElementById('loginForm');
const adminButton = document.getElementById('adminButton');
const terminalButton = document.getElementById('terminalButton');
const messageArea = document.getElementById('messageArea');

// ------------------ Função para exibir mensagens na tela ------------------
function showMessage(text, type = 'info') {
    if (messageArea) {
        messageArea.textContent = text;
        messageArea.classList.remove('message-type-success', 'message-type-error', 'message-type-info', 'visible');
        if (type === 'success') {
            messageArea.classList.add('message-type-success');
        } else if (type === 'error') {
            messageArea.classList.add('message-type-error');
        } else {
            messageArea.classList.add('message-type-info');
        }
        requestAnimationFrame(() => {
            messageArea.classList.add('visible');
        });
        // setTimeout(() => { messageArea.classList.remove('visible'); }, 7000); // Opcional: auto-hide
    } else {
        alert(text);
    }
}

// ------------------ Função para buscar informações do Operador (AJUSTADA para objeto único) ---
const buscarInfoOperador = async (operatorCode) => {
    // IMPORTANTE: Use o URL base da sua API Django.
    // A URL '/api/v1/workforce/${operatorCode}' foi baseada nos seus logs de erro anteriores.
    const apiUrl = `http://127.0.0.1:8000/api/v1/workforce/${encodeURIComponent(operatorCode)}/`; // Verifique se esta URL está 100% correta

    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            let errorMsg = `Operador não encontrado ou erro na API (HTTP ${response.status})`;
            try { const errorData = await response.json(); errorMsg = errorData.detail || errorData.erro || errorMsg; } catch (e) {}
            console.error('Falha ao buscar operador:', errorMsg);
            return { error: errorMsg, source: 'operador' };
        }
        const apiData = await response.json();

        if (apiData.erro) {
            console.error('Erro da API (Operador):', apiData.erro);
            return { error: apiData.erro, source: 'operador' };
        } else if (Array.isArray(apiData) && apiData.length > 0) { // Se retornar array (pouco provável agora)
            const operatorData = apiData[0];
            return { operatorName: operatorData.name, data: operatorData }; // Assumindo que 'nome' é a propriedade
        } else if (typeof apiData === 'object' && apiData !== null && !Array.isArray(apiData) && apiData.hasOwnProperty('name')) { // Mudado de 'nome' para 'name' baseado no seu último log
            // A API retornou um único objeto diretamente
            return { operatorName: apiData.name, data: apiData }; // Use 'apiData.name'
        } else {
            console.error('Formato de dados inesperado ou operador não encontrado (verifique a propriedade do nome):', apiData);
            return { error: 'Operador não encontrado ou formato de dados inesperado (verifique JS).', source: 'operador' };
        }
    } catch (error) {
        console.error('Erro de rede ao buscar operador:', error);
        return { error: 'Erro de rede ao buscar dados do operador.', source: 'operador' };
    }
};
// Em login.js

// ... (resto do seu código: seletores, showMessage, buscarInfoOperador) ...

// ------------------ Função para buscar informações do Equipamento (REFINADA) ---
const buscarInfoEquipamento = async (equipmentCode) => {
    // IMPORTANTE: Use o URL base da sua API Django.
    // A URL '/api/v1/equipments/${equipmentCode}/' foi baseada nos seus logs de erro e na necessidade da barra final.
    const apiUrl = `http://127.0.0.1:8000/api/v1/equipments/${encodeURIComponent(equipmentCode)}/`;

    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            let errorMsg = `Equipamento não encontrado ou erro na API (HTTP ${response.status})`;
            try { const errorData = await response.json(); errorMsg = errorData.detail || errorData.erro || errorMsg; } catch (e) {}
            console.error('Falha ao buscar equipamento:', errorMsg);
            return { error: errorMsg, source: 'equipamento' };
        }
        // Renomeado de dataArray para apiData para clareza, já que esperamos um objeto.
        const apiData = await response.json();

        // Verifica se a API retornou um erro explícito no JSON (ex: { "erro": "mensagem" })
        if (apiData.erro) {
            console.error('Erro da API (Equipamento):', apiData.erro);
            return { error: apiData.erro, source: 'equipamento' };
        }
        // Verifica se é um objeto único e se possui a propriedade 'description'
        else if (typeof apiData === 'object' && apiData !== null && !Array.isArray(apiData) && apiData.hasOwnProperty('description')) {
            // A API retornou um único objeto diretamente com a descrição.
            return { equipmentName: apiData.description, data: apiData };
        }
        // Se não for nenhum dos formatos esperados (nem erro explícito, nem objeto com 'description')
        else {
            console.error('Formato de dados inesperado ou equipamento não encontrado:', apiData);
            return { error: 'Equipamento não encontrado ou formato de dados inesperado.', source: 'equipamento' };
        }
    } catch (error) {
        console.error('Erro de rede ao buscar equipamento:', error);
        return { error: 'Erro de rede ao buscar dados do equipamento.', source: 'equipamento' };
    }
};

// ... (resto do seu código: EventListener do loginForm, EventListeners para outros botões) ...
// ------------------ Event Listener para o Formulário de Login ------------------
if (loginForm) {
    loginForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        showMessage('Processando...', 'info'); // Usando sua função showMessage

        const operatorCodeInput = document.getElementById('operatorCode');
        const equipmentCodeInput = document.getElementById('equipmentCode');
        const operatorCode = operatorCodeInput ? operatorCodeInput.value.trim() : '';
        const equipmentCode = equipmentCodeInput ? equipmentCodeInput.value.trim() : '';

        const submitButton = loginForm.querySelector('button[type="submit"]'); // Assumindo que é o botão "Entrar (Estação Dedicada)"
        if(submitButton) submitButton.disabled = true;

        // Limpa sessionStorage de logins anteriores antes de tentar um novo login de estação
        sessionStorage.removeItem('operatorCode');
        sessionStorage.removeItem('operatorName');
        sessionStorage.removeItem('operatorData');
        sessionStorage.removeItem('equipmentCode');
        sessionStorage.removeItem('equipmentName');
        sessionStorage.removeItem('equipmentData');
        sessionStorage.removeItem('loginType'); // Será definido com base no sucesso

        let loginSuccess = false;

        if (operatorCode && equipmentCode) {
            // CASO 1: Ambos os campos preenchidos
            console.log('Buscando dados para Operador:', operatorCode, 'e Equipamento:', equipmentCode);
            const [resultadoOperador, resultadoEquipamento] = await Promise.all([
                buscarInfoOperador(operatorCode),
                buscarInfoEquipamento(equipmentCode)
            ]);

            let mensagensErro = [];
            if (resultadoOperador.error) mensagensErro.push(`Operador: ${resultadoOperador.error}`);
            if (resultadoEquipamento.error) mensagensErro.push(`Equipamento: ${resultadoEquipamento.error}`);

            if (mensagensErro.length > 0) {
                showMessage(`Erro ao buscar informações:\n- ${mensagensErro.join('\n- ')}`, 'error');
            } else {
                sessionStorage.setItem('loginType', 'station');
                sessionStorage.setItem('operatorCode', operatorCode);
                sessionStorage.setItem('operatorName', resultadoOperador.operatorName);
                sessionStorage.setItem('operatorData', JSON.stringify(resultadoOperador.data));
                sessionStorage.setItem('equipmentCode', equipmentCode);
                sessionStorage.setItem('equipmentName', resultadoEquipamento.equipmentName);
                sessionStorage.setItem('equipmentData', JSON.stringify(resultadoEquipamento.data));

                showMessage(`Acesso liberado!\nOperador: ${resultadoOperador.operatorName}\nEquipamento: ${resultadoEquipamento.equipmentName}\nRedirecionando...`, 'success');
                loginSuccess = true;
            }
        } else if (operatorCode && !equipmentCode) {
            // CASO 2: Apenas Operador preenchido
            console.log('Buscando dados para Operador:', operatorCode);
            const resultadoOperador = await buscarInfoOperador(operatorCode);

            if (resultadoOperador.error) {
                showMessage(`Operador: ${resultadoOperador.error}`, 'error');
            } else {
                sessionStorage.setItem('loginType', 'station'); // Ainda é 'station', mas parcial
                sessionStorage.setItem('operatorCode', operatorCode);
                sessionStorage.setItem('operatorName', resultadoOperador.operatorName);
                sessionStorage.setItem('operatorData', JSON.stringify(resultadoOperador.data));
                // equipmentCode, equipmentName, equipmentData não serão definidos

                showMessage(`Operador ${resultadoOperador.operatorName} identificado. Equipamento será solicitado depois.\nRedirecionando...`, 'success');
                loginSuccess = true;
            }
        } else if (!operatorCode && equipmentCode) {
            // CASO 3: Apenas Equipamento preenchido
            console.log('Buscando dados para Equipamento:', equipmentCode);
            const resultadoEquipamento = await buscarInfoEquipamento(equipmentCode);

            if (resultadoEquipamento.error) {
                showMessage(`Equipamento: ${resultadoEquipamento.error}`, 'error');
            } else {
                sessionStorage.setItem('loginType', 'station'); // Ainda é 'station', mas parcial
                sessionStorage.setItem('equipmentCode', equipmentCode);
                sessionStorage.setItem('equipmentName', resultadoEquipamento.equipmentName);
                sessionStorage.setItem('equipmentData', JSON.stringify(resultadoEquipamento.data));
                // operatorCode, operatorName, operatorData não serão definidos

                showMessage(`Equipamento ${resultadoEquipamento.equipmentName} identificado. Operador será solicitado depois.\nRedirecionando...`, 'success');
                loginSuccess = true;
            }
        } else {
            // CASO 4: Nenhum campo preenchido
            showMessage('Por favor, preencha Operador e/ou Equipamento, ou use o botão "Modo Terminal".', 'error');
        }

        if(submitButton) submitButton.disabled = false;

        if (loginSuccess) {
            setTimeout(() => {
                window.location.href = 'home.html'; // Ou o caminho correto para sua home.html
            }, 2000); // Delay para o usuário ler a mensagem
        }
    });
}

// ------------------ Event Listeners para outros botões ------------------
if (adminButton) {
    adminButton.addEventListener('click', function() {
        console.log('Botão Admin clicado');
        showMessage('Redirecionando para a área de Administração...', 'info');
        // window.location.href = '/admin/';
        if (terminalButton) terminalButton.disabled = true;
        setTimeout(() => { window.location.href = 'http://127.0.0.1:8000/admin/'; }, 1000);
    });
}

// Modifique esta parte conforme a Opção A ou B da nossa discussão anterior sobre o login de terminal
if (terminalButton) {
    terminalButton.addEventListener('click', function() { // Opção B: Sem chamada de API no clique
        console.log('Botão Terminal clicado - entrando em modo terminal direto.');
        showMessage('Entrando como Terminal... Redirecionando...', 'info');

        sessionStorage.setItem('loginType', 'terminal');
        sessionStorage.removeItem('operatorCode');
        sessionStorage.removeItem('operatorName');
        sessionStorage.removeItem('operatorData');
        sessionStorage.removeItem('equipmentCode');
        sessionStorage.removeItem('equipmentName');
        sessionStorage.removeItem('equipmentData');

        if (terminalButton) terminalButton.disabled = true;
        setTimeout(() => { window.location.href = 'home.html'; }, 1000);
    });
}