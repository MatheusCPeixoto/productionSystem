// ../script/home.js

document.addEventListener('DOMContentLoaded', () => {
    // --- SELEÇÃO DE ELEMENTOS DO DOM ---
    const userInfoDisplay = document.getElementById('userInfoDisplay');
    const triggerOpenOrderModalButton = document.getElementById('triggerOpenOrderModalButton');
    const ongoingTasksContainer = document.getElementById('ongoingTasksCardsContainer');
    const noOngoingTasksMessage = document.getElementById('noOngoingTasksMessage');
    const mainMessageArea = document.getElementById('mainMessageArea');
    const searchInputOngoingTasks = document.getElementById('searchInputOngoingTasks');
    const changeOpEqButton = document.getElementById('changeOpEqButton');
    const switchModeButton = document.getElementById('switchModeButton');
    const switchModeButtonText = document.getElementById('switchModeButtonText');
    const multiOrderToggle = document.getElementById('multiOrderToggle');

    // Modais e seus componentes
    const orderInteractionModal = document.getElementById('orderInteractionModal');
    const opEqModal = document.getElementById('opEqModal');
    const stopReasonModal = document.getElementById('stopReasonModal');
    const finalizeTaskModal = document.getElementById('finalizeTaskModal');
    const ncModal = document.getElementById('ncModal');

    let currentOrderCodeForProcessing = null;
    let fetchedTasksCache = [];

    // --- FUNÇÃO PARA EXIBIR MENSAGENS ---
    function showMessage(text, type = 'info', area = mainMessageArea) {
        if (!area) {
            console.warn("Área de mensagem não definida:", text);
            alert(text);
            return;
        }
        area.textContent = text;
        area.className = 'p-3 my-2 rounded-md text-center text-sm transition-opacity duration-300';
        area.style.visibility = 'hidden';
        area.style.opacity = '0';

        if (type === 'success') area.classList.add('message-type-success');
        else if (type === 'error') area.classList.add('message-type-error');
        else area.classList.add('message-type-info');

        if (text) {
            area.style.visibility = 'visible';
            area.style.opacity = '1';
        }

        const isMainMsg = area === mainMessageArea;
        if (text && (type !== 'error' || isMainMsg)) {
             setTimeout(() => {
                area.style.opacity = '0';
                setTimeout(() => { area.style.visibility = 'hidden'; }, 300);
            }, isMainMsg ? 5000 : 4000);
        }
    }

    // --- FUNÇÕES DE BUSCA DE DADOS (API Calls) ---
    const buscarInfoOperador = async (operatorCode) => {
        const apiUrl = `http://127.0.0.1:8000/api/v1/workforce/${encodeURIComponent(operatorCode)}/`;
        try {
            const response = await fetch(apiUrl);
            if (!response.ok) { throw new Error(`Operador não encontrado (HTTP ${response.status})`); }
            const apiData = await response.json();
            if (apiData.erro) { throw new Error(apiData.erro); }
            if (apiData.hasOwnProperty('name')) { return { operatorName: apiData.name, data: apiData }; }
            throw new Error("Formato de dados do operador inesperado.");
        } catch (error) { console.error('Erro (Operador):', error); return { error: error.message, code: operatorCode }; }
    };

    const buscarInfoEquipamento = async (equipmentCode) => {
        const apiUrl = `http://127.0.0.1:8000/api/v1/equipments/${encodeURIComponent(equipmentCode)}/`;
        try {
            const response = await fetch(apiUrl);
            if (!response.ok) { throw new Error(`Equipamento não encontrado (HTTP ${response.status})`); }
            const apiData = await response.json();
            if (apiData.erro) { throw new Error(apiData.erro); }
            if (apiData.hasOwnProperty('description')) { return { equipmentName: apiData.description, data: apiData }; }
            throw new Error("Formato de dados do equipamento inesperado.");
        } catch (error) { console.error('Erro (Equipamento):', error); return { error: error.message, code: equipmentCode }; }
    };

    async function loadReasonsToSelect(reasonType) {
        let apiUrl = '', selectElement, modalMessageArea;
        if (reasonType === 'stop') {
            apiUrl = 'http://127.0.0.1:8000/api/v1/stop-reason/?is_active=1';
            selectElement = document.getElementById('stopReasonSelect');
            modalMessageArea = document.getElementById('stopReasonModalMessageArea');
        } else if (reasonType === 'nc') {
            apiUrl = 'http://127.0.0.1:8000/api/v1/non-conformance/?is_active=1';
            selectElement = document.getElementById('ncReasonSelect');
            modalMessageArea = document.getElementById('ncModalMessageArea');
        } else { return; }
        if (!selectElement) return;
        showMessage('Carregando motivos...', 'info', modalMessageArea);
        selectElement.innerHTML = '<option value="">Carregando...</option>';
        try {
            const response = await fetch(apiUrl);
            if (!response.ok) throw new Error(`Falha ao carregar da API (HTTP ${response.status})`);
            const reasons = await response.json();
            const reasonList = Array.isArray(reasons) ? reasons : reasons.results;
            if (!Array.isArray(reasonList)) throw new Error("Formato de resposta da API de motivos inválido.");
            selectElement.innerHTML = '<option value="">Selecione um motivo...</option>';
            reasonList.forEach(reason => {
                const option = document.createElement('option');
                option.value = reason.code;
                option.textContent = reason.description;
                selectElement.appendChild(option);
            });
            showMessage('', 'info', modalMessageArea);
        } catch (error) {
            console.error(`Erro ao carregar motivos de ${apiUrl}:`, error);
            showMessage('Falha ao carregar motivos.', 'error', modalMessageArea);
            selectElement.innerHTML = '<option value="">Erro ao carregar</option>';
        }
    }

    // --- LÓGICA DE RENDERIZAÇÃO E UI ---
    function loadUserInfo() {
        const loginType = sessionStorage.getItem('loginType');
        const operatorCode = sessionStorage.getItem('operatorCode');
        const equipmentCode = sessionStorage.getItem('equipmentCode');
        let displayText = 'Terminal', showChangeOpEq = false, switchButtonText = 'Modo Estação', enableMultiOrder = false;

        if (loginType === 'station') {
            const operatorName = sessionStorage.getItem('operatorName') || 'Operador Indef.';
            const equipmentName = sessionStorage.getItem('equipmentName') || 'Equip. Indef.';
            displayText = `${operatorName} @ ${equipmentName}`;
            showChangeOpEq = true;
            switchButtonText = 'Modo Terminal';
            if (operatorCode || equipmentCode) {
                enableMultiOrder = true;
            }
        }

        if (userInfoDisplay) userInfoDisplay.textContent = displayText;
        if (switchModeButtonText) switchModeButtonText.textContent = switchButtonText;
        if (changeOpEqButton) changeOpEqButton.style.display = showChangeOpEq ? 'flex' : 'none';
        if (multiOrderToggle) {
            multiOrderToggle.disabled = !enableMultiOrder;
            const label = multiOrderToggle.closest('label');
            if (label) {
                label.classList.toggle('opacity-50', !enableMultiOrder);
                label.classList.toggle('cursor-not-allowed', !enableMultiOrder);
            }
            if (!enableMultiOrder) {
                multiOrderToggle.checked = false;
                sessionStorage.setItem('multiOrderModeEnabled', 'false');
            } else {
                multiOrderToggle.checked = sessionStorage.getItem('multiOrderModeEnabled') === 'true';
            }
        }
    }

    async function fetchOngoingTasks() {
        showMessage('Buscando apontamentos...', 'info', mainMessageArea);
        const apiUrl = 'http://127.0.0.1:8000/api/v1/order-activity-progress/';
        try {
            const response = await fetch(apiUrl);
            if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);
            fetchedTasksCache = await response.json();
            if (!Array.isArray(fetchedTasksCache)) { fetchedTasksCache = []; throw new Error("Formato da resposta da API inválido."); }
            renderOngoingTasks(fetchedTasksCache);
            if (fetchedTasksCache.length > 0 && mainMessageArea.textContent.includes('Buscando')) {
                 showMessage('Apontamentos carregados.', 'success', mainMessageArea);
            }
        } catch (error) {
            console.error("Erro ao buscar tarefas:", error);
            showMessage(`Falha ao carregar apontamentos: ${error.message}`, 'error', mainMessageArea);
            fetchedTasksCache = [];
            renderOngoingTasks([]);
        }
    }

    function renderOngoingTasks(tasks) {
        if(!ongoingTasksContainer || !noOngoingTasksMessage) return;
        ongoingTasksContainer.innerHTML = '';
        if (tasks && tasks.length > 0) {
            noOngoingTasksMessage.classList.add('hidden');
            const cardElements = tasks.map(task => createCardElement(task));
            cardElements.forEach(card => ongoingTasksContainer.appendChild(card));
        } else {
            noOngoingTasksMessage.textContent = "Nenhum apontamento em andamento.";
            noOngoingTasksMessage.classList.remove('hidden');
        }
        filterOngoingTasks();
    }

    function createCardElement(task) {
        const operatorNames = (task.active_workforce_log || []).map(log => log.workforce_name || 'Nome não encontrado');
        const equipmentNames = (task.active_equipment_log || []).map(log => log.equipment_description || 'Descrição não encontrada');
        const card = document.createElement('div');
        card.className = 'bg-white p-5 rounded-xl shadow-lg task-card flex flex-col justify-between';
        card.dataset.orderId = task.order_code;
        card.dataset.activityId = task.code;
        const status = task.status || (task.end_date === null ? 'Em Andamento' : 'Finalizado');
        card.dataset.status = status.toLowerCase();
        card.dataset.searchableContent = `${task.order_code} ${task.activity?.description} ${operatorNames.join(' ')} ${equipmentNames.join(' ')}`.toLowerCase();

        let statusVisualClass = '', statusBlinkingClass = '';
        if (status === 'Em Andamento') { statusVisualClass = 'bg-green-100 text-green-800'; }
        else if (status === 'Parado') { statusVisualClass = 'bg-yellow-100 text-yellow-700'; statusBlinkingClass = 'status-parado-blinking'; }
        else if (status === 'Finalizado') { statusVisualClass = 'bg-blue-100 text-blue-800'; }
        else { statusVisualClass = 'bg-gray-100 text-gray-600'; }

        card.innerHTML = `
            <div>
                <div class="mb-3 text-center"><span class="px-3 py-1 inline-flex text-md leading-tight font-bold rounded-full ${statusVisualClass} ${statusBlinkingClass}">${status}</span></div>
                <div class="mb-3 text-sm">
                    <p class="text-gray-800 truncate" title="Ordem: ${task.order_code} - Atividade: ${task.activity?.description}">
                        <strong class="font-semibold text-gray-500">Cód:</strong> ${task.order_code} <span class="text-gray-400 mx-1">|</span> <strong class="font-semibold text-gray-500">Seq:</strong> ${task.sequence}<br>
                        <strong class="font-semibold text-gray-500">Ativ:</strong> ${task.activity?.description || 'N/A'}
                    </p>
                </div>
                <div class="mb-3 text-sm"><p class="text-gray-600"><i class="fas fa-calendar-alt mr-1 text-gray-400"></i><strong class="text-gray-500">Início:</strong> ${task.start_date ? new Date(task.start_date).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }) : '-'}</p></div>
                <div class="grid grid-cols-2 gap-4 border-t border-b py-3 my-3">
                    <div>
                        <h4 class="font-semibold text-gray-600 text-sm mb-1"><i class="fas fa-users-cog mr-1"></i> Operadores</h4>
                        <ul class="list-disc list-inside text-gray-700 text-sm space-y-1">${operatorNames.length > 0 ? operatorNames.map(name => `<li class="truncate" title="${name}">${name}</li>`).join('') : '<li>Nenhum</li>'}</ul>
                    </div>
                    <div>
                        <h4 class="font-semibold text-gray-600 text-sm mb-1"><i class="fas fa-cogs mr-1"></i> Equipamentos</h4>
                        <ul class="list-disc list-inside text-gray-700 text-sm space-y-1">${equipmentNames.length > 0 ? equipmentNames.map(name => `<li class="truncate" title="${name}">${name}</li>`).join('') : '<li>Nenhum</li>'}</ul>
                    </div>
                </div>
            </div>
            <div class="mt-auto flex flex-wrap justify-around gap-2">
                <button title="Retomar" class="btn-action-card text-blue-600 hover:text-blue-900 p-3 rounded-lg flex items-center justify-center w-12 h-12 action-resume ${status !== 'Parado' ? 'opacity-50 cursor-not-allowed' : ''}" ${status !== 'Parado' ? 'disabled' : ''}><i class="fas fa-play-circle fa-xl"></i></button>
                <button title="Parada" class="btn-action-card text-yellow-500 hover:text-yellow-700 p-3 rounded-lg flex items-center justify-center w-12 h-12 action-stop ${status !== 'Em Andamento' ? 'opacity-50 cursor-not-allowed' : ''}" ${status !== 'Em Andamento' ? 'disabled' : ''}><i class="fas fa-pause-circle fa-xl"></i></button>
                <button title="Finalizar" class="btn-action-card text-green-500 hover:text-green-700 p-3 rounded-lg flex items-center justify-center w-12 h-12 action-finish ${status === 'Finalizado' ? 'opacity-50 cursor-not-allowed' : ''}" ${status === 'Finalizado' ? 'disabled' : ''}><i class="fas fa-check-circle fa-xl"></i></button>
                <button title="Não Conformidade" class="btn-action-card text-red-500 hover:text-red-700 p-3 rounded-lg flex items-center justify-center w-12 h-12 action-nc"><i class="fas fa-exclamation-triangle fa-xl"></i></button>
            </div>
        `;
        return card;
    }

    function filterOngoingTasks() {
        if (!searchInputOngoingTasks || !ongoingTasksContainer || !noOngoingTasksMessage) return;
        const searchTerm = searchInputOngoingTasks.value.toLowerCase();
        const cards = ongoingTasksContainer.querySelectorAll('.task-card');
        let visibleCardsCount = 0;
        cards.forEach(card => {
            const searchableText = card.dataset.searchableContent || '';
            if (searchableText.includes(searchTerm)) { card.style.display = 'flex'; visibleCardsCount++; }
            else { card.style.display = 'none'; }
        });
        if (fetchedTasksCache.length === 0) { noOngoingTasksMessage.textContent = "Nenhum apontamento em andamento."; noOngoingTasksMessage.style.display = 'block'; }
        else if (visibleCardsCount === 0 && searchTerm) { noOngoingTasksMessage.textContent = "Nenhum apontamento encontrado para sua busca."; noOngoingTasksMessage.style.display = 'block'; }
        else { noOngoingTasksMessage.style.display = 'none'; }
    }

    function openModal(modal) { if (modal) modal.classList.add('active'); }
    function closeModal(modal) { if (modal) modal.classList.remove('active'); }

    // --- LÓGICA PARA ABRIR ORDEM E MODAIS DE AÇÃO ---
    function displayOrderCodeInputInModal() {
        if (!orderInteractionModal) return;
        const modalTitle = orderInteractionModal.querySelector('#orderInteractionModalTitle');
        const modalContent = orderInteractionModal.querySelector('#orderInteractionModalContent');
        const modalMsgArea = orderInteractionModal.querySelector('#orderInteractionModalMessageArea');
        if(modalTitle) modalTitle.textContent = 'Abrir Ordem de Produção';
        if(modalContent) modalContent.innerHTML = `<form id="modalOrderCodeForm" class="space-y-4"><div><label for="modalOrderCode" class="block text-sm font-medium text-gray-700 mb-1">Código da Ordem:</label><input type="text" id="modalOrderCode" class="w-full p-2 border border-gray-300 rounded-md" required></div><button type="submit" class="w-full bg-sky-600 text-white font-semibold py-2 px-4 rounded-md">Buscar Etapas</button></form>`;
        if(modalMsgArea) showMessage('', 'info', modalMsgArea);
        openModal(orderInteractionModal);
        const form = document.getElementById('modalOrderCodeForm');
        form.replaceWith(form.cloneNode(true));
        document.getElementById('modalOrderCodeForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const orderCode = document.getElementById('modalOrderCode').value.trim();
            if(orderCode) { currentOrderCodeForProcessing = orderCode; await validateLoginModeAndProceed(orderCode); }
            else { showMessage('Insira um código de ordem.', 'error', modalMsgArea); }
        });
    }

    async function validateLoginModeAndProceed(orderCode) {
        const loginType = sessionStorage.getItem('loginType');
        let opCode = sessionStorage.getItem('operatorCode'), eqCode = sessionStorage.getItem('equipmentCode');
        let needsOp = !opCode, needsEq = !eqCode;
        if (loginType === 'terminal') { needsOp = true; needsEq = true; }
        if (needsOp || needsEq) { openOpEqModalForChanges(needsOp, needsEq); }
        else { await fetchOrderStepsForDisplay(orderCode, opCode, eqCode); }
    }

    async function fetchOrderStepsForDisplay(orderCode, operatorCode, equipmentCode) {
        const modalTitle = document.getElementById('orderInteractionModalTitle');
        const modalContent = document.getElementById('orderInteractionModalContent');
        const modalMsgArea = document.getElementById('orderInteractionModalMessageArea');
        if (!orderInteractionModal || !modalTitle || !modalContent) return;
        if (!orderCode) { showMessage('Código da ordem não fornecido.', 'error', modalMsgArea); return; }
        const apiUrl = `http://127.0.0.1:8000/api/v1/order-items/?order_code=${encodeURIComponent(orderCode)}`;
        modalTitle.textContent = `Etapas da Ordem: ${orderCode}`;
        modalContent.innerHTML = `<p class="text-gray-500 p-4 text-center">Buscando etapas...</p>`;
        openModal(orderInteractionModal);
        try {
            const response = await fetch(apiUrl);
            if (!response.ok) throw new Error(`Erro ao buscar etapas: ${response.statusText}`);
            const orderItems = await response.json();
            const allSteps = Array.isArray(orderItems) ? orderItems.flatMap(item => (item.structure_activities || []).map(activity => ({ ...activity, order_code: item.order_code, company_code: item.company_code, branch_code: item.branch_code }))) : [];
            if (allSteps.length > 0) {
                modalContent.innerHTML = `<p class="text-sm text-gray-600 mb-3">Selecione a etapa para iniciar:</p><div class="space-y-2 max-h-60 overflow-y-auto">${allSteps.map(step => `<button data-step-info='${JSON.stringify(step)}' class="w-full text-left p-3 bg-gray-100 hover:bg-sky-100 rounded-md order-step-button"><strong>${step.activity_description}</strong> <span class="text-xs text-gray-500">(Seq: ${step.sequence})</span></button>`).join('')}</div>`;
                if(modalMsgArea) showMessage('', 'info', modalMsgArea);
                modalContent.querySelectorAll('.order-step-button').forEach(button => {
                    button.addEventListener('click', async () => {
                        const stepInfo = JSON.parse(button.dataset.stepInfo);
                        button.disabled = true; button.innerHTML += ' <i class="fas fa-spinner fa-spin"></i>';
                        await startActivityAppointment(stepInfo);
                    });
                });
            } else { modalContent.innerHTML = `<p class="text-red-500 p-4 text-center">Nenhuma etapa encontrada para esta ordem.</p>`; }
        } catch (error) {
            console.error('Erro ao buscar etapas:', error);
            modalContent.innerHTML = `<p class="text-red-500 p-4 text-center">Falha ao carregar etapas.</p>`;
            if(modalMsgArea) showMessage('Falha ao carregar etapas.', 'error', modalMsgArea);
        }
    }

    async function startActivityAppointment(stepInfo) {
        const operatorCode = sessionStorage.getItem('operatorCode');
        const equipmentCode = sessionStorage.getItem('equipmentCode');
        const modalMsgArea = document.getElementById('orderInteractionModalMessageArea');
        showMessage('Iniciando apontamento...', 'info', modalMsgArea);
        const payload = {
            company_code: stepInfo.company_code, branch_code: stepInfo.branch_code,
            order_code: stepInfo.order_code, activity_code: stepInfo.activity_code,
            sequence: stepInfo.sequence, operator_code: operatorCode, equipment_code: equipmentCode,
        };
        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/start-activity/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
            if (!response.ok) {
                const errorData = await response.json();
                const errorMessage = errorData.error || errorData.detail || JSON.stringify(errorData);
                throw new Error(`Falha ao iniciar apontamento: ${errorMessage}`);
            }
            const result = await response.json();
            showMessage(result.message || 'Apontamento iniciado com sucesso!', 'success', mainMessageArea);
            closeModal(orderInteractionModal);
            await fetchOngoingTasks();
        } catch (error) {
            console.error("Erro na sequência de apontamento:", error);
            showMessage(`Erro: ${error.message}`, 'error', modalMsgArea);
            const failedButton = document.querySelector(`button[data-step-info*='"code":${stepInfo.code}']`);
            if (failedButton) { failedButton.disabled = false; failedButton.querySelector('i.fa-spinner')?.remove(); }
        }
    }

    async function finalizeActivityAppointment(activityId, quantity) {
        const apiUrl = `http://127.0.0.1:8000/api/v1/order-activity-progress/${activityId}/`;
        const modalMsgArea = document.getElementById('finalizeTaskModalMessageArea');
        showMessage('Finalizando apontamento...', 'info', modalMsgArea);
        const payload = { quantity: quantity };
        try {
            const response = await fetch(apiUrl, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
            if (!response.ok) {
                const errorData = await response.json();
                const errorMessage = errorData.error || errorData.detail || JSON.stringify(errorData);
                throw new Error(`Falha ao finalizar: ${errorMessage}`);
            }
            const result = await response.json();
            showMessage(result.message || 'Apontamento finalizado com sucesso!', 'success', mainMessageArea);
            closeModal(document.getElementById('finalizeTaskModal'));
            await fetchOngoingTasks();
        } catch (error) {
            console.error("Erro ao finalizar apontamento:", error);
            showMessage(`Erro: ${error.message}`, 'error', modalMsgArea);
        }
    }

    async function stopActivity(activityId, reasonId, showSuccessMsg = true) {
        const apiUrl = `http://127.0.0.1:8000/api/v1/order-activity-progress/${activityId}/stop/`;
        const modal = document.getElementById('stopReasonModal');
        const modalMsgArea = modal ? modal.querySelector('#stopReasonModalMessageArea') : mainMessageArea;
        showMessage(`Registrando parada...`, 'info', modalMsgArea);
        try {
            const response = await fetch(apiUrl, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ stop_reason_code: reasonId }) });
            if (!response.ok) {
                const errorData = await response.json(); throw new Error(errorData.error || 'Falha ao registrar parada.');
            }
            const result = await response.json();
            if (showSuccessMsg) { showMessage(result.message, 'success', mainMessageArea); }
            if (modal) closeModal(modal);
            return { success: true };
        } catch (error) {
            console.error("Erro ao parar atividade:", error); showMessage(`Erro: ${error.message}`, 'error', modalMsgArea);
            return { success: false, error: error.message };
        }
    }

    async function resumeActivity(activityIdToResume) {
        const isMultiOrderMode = sessionStorage.getItem('multiOrderModeEnabled') === 'true';
        if (isMultiOrderMode) {
            const activeTask = fetchedTasksCache.find(task => (task.status || (task.end_date === null ? 'Em Andamento' : 'Finalizado')) === 'Em Andamento' && task.code.toString() !== activityIdToResume.toString());
            if (activeTask) {
                showMessage(`Modo Múltipla Ordem: Parando tarefa ativa ${activeTask.code}...`, 'info', mainMessageArea);
                const stopResult = await stopActivity(activeTask.code, '20', false);
                if (!stopResult.success) {
                    showMessage(`Falha ao parar a tarefa anterior (${activeTask.code}). Ação cancelada.`, 'error', mainMessageArea);
                    await fetchOngoingTasks(); // Recarrega para refletir o estado real
                    return;
                }
            }
        }
        const apiUrl = `http://127.0.0.1:8000/api/v1/order-activity-progress/${activityIdToResume}/resume/`;
        showMessage(`Retomando apontamento ${activityIdToResume}...`, 'info', mainMessageArea);
        try {
            const response = await fetch(apiUrl, { method: 'POST' });
            if (!response.ok) {
                const errorData = await response.json(); throw new Error(errorData.error || 'Falha ao retomar apontamento.');
            }
            const result = await response.json();
            showMessage(result.message, 'success', mainMessageArea);
            await fetchOngoingTasks();
        } catch (error) {
            console.error("Erro ao retomar atividade:", error);
            showMessage(`Erro: ${error.message}`, 'error', mainMessageArea);
            await fetchOngoingTasks();
        }
    }

    function openOpEqModalForChanges(requireOperator, requireEquipment) {
        if (!opEqModal) return;
        const opInputGroup = opEqModal.querySelector('#operatorInputGroup'), opInput = opEqModal.querySelector('#modalOperatorCode');
        const eqInputGroup = opEqModal.querySelector('#equipmentInputGroup'), eqInput = opEqModal.querySelector('#modalEquipmentCode');
        opInputGroup.style.display = 'block'; opInput.value = sessionStorage.getItem('operatorCode') || ''; opInput.required = requireOperator;
        eqInputGroup.style.display = 'block'; eqInput.value = sessionStorage.getItem('equipmentCode') || ''; eqInput.required = requireEquipment;
        showMessage('Insira os códigos necessários.', 'info', opEqModal.querySelector('#opEqModalMessageArea'));
        openModal(opEqModal);
    }

    // --- EVENT LISTENERS ---
    if (triggerOpenOrderModalButton) triggerOpenOrderModalButton.addEventListener('click', displayOrderCodeInputInModal);
    if (searchInputOngoingTasks) searchInputOngoingTasks.addEventListener('input', filterOngoingTasks);
    [document.getElementById('closeOrderInteractionModal'), document.getElementById('closeOpEqModal'), document.getElementById('closeStopReasonModal'), document.getElementById('closeFinalizeTaskModal'), document.getElementById('closeNcModal')]
        .forEach(btn => { if(btn) btn.addEventListener('click', () => closeModal(btn.closest('.modal'))) });

    if (changeOpEqButton) changeOpEqButton.addEventListener('click', () => { currentOrderCodeForProcessing = null; openOpEqModalForChanges(true, true); });
    if (switchModeButton) {
        switchModeButton.addEventListener('click', () => {
            const currentLoginType = sessionStorage.getItem('loginType');
            currentOrderCodeForProcessing = null;
            if (currentLoginType === 'station') {
                sessionStorage.setItem('loginType', 'terminal');
                ['operatorCode', 'operatorName', 'operatorData', 'equipmentCode', 'equipmentName', 'equipmentData'].forEach(item => sessionStorage.removeItem(item));
                loadUserInfo(); showMessage('Modo alterado para Terminal.', 'success', mainMessageArea);
            } else {
                showMessage('Para Modo Estação, informe Operador e Equipamento.', 'info', mainMessageArea);
                openOpEqModalForChanges(true, true);
            }
        });
    }

    if (multiOrderToggle) {
        multiOrderToggle.addEventListener('change', (event) => {
            const isEnabled = event.target.checked;
            sessionStorage.setItem('multiOrderModeEnabled', isEnabled);
            showMessage(`Modo Múltipla Ordem ${isEnabled ? 'ATIVADO' : 'DESATIVADO'}.`, 'info', mainMessageArea);
        });
    }

    if (opEqForm) {
        opEqForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const submitBtn = opEqForm.querySelector('button[type="submit"]');
            const msgArea = opEqForm.querySelector('#opEqModalMessageArea');
            if(submitBtn) submitBtn.disabled = true;
            showMessage('Validando...', 'info', msgArea);
            const opCodeRequired = opEqForm.querySelector('#modalOperatorCode').required, eqCodeRequired = opEqForm.querySelector('#modalEquipmentCode').required;
            const inputOpCode = opCodeRequired ? opEqForm.querySelector('#modalOperatorCode').value.trim() : sessionStorage.getItem('operatorCode');
            const inputEqCode = eqCodeRequired ? opEqForm.querySelector('#modalEquipmentCode').value.trim() : sessionStorage.getItem('equipmentCode');
            if (opCodeRequired && !inputOpCode) { showMessage('Cód. Operador é obrigatório.', 'error', msgArea); if(submitBtn) submitBtn.disabled = false; return; }
            if (eqCodeRequired && !inputEqCode) { showMessage('Cód. Equipamento é obrigatório.', 'error', msgArea); if(submitBtn) submitBtn.disabled = false; return; }
            let opDetails = { operatorName: sessionStorage.getItem('operatorName'), data: JSON.parse(sessionStorage.getItem('operatorData') || 'null') };
            let eqDetails = { equipmentName: sessionStorage.getItem('equipmentName'), data: JSON.parse(sessionStorage.getItem('equipmentData') || 'null') };
            let proceed = true;
            if (inputOpCode && (inputOpCode !== sessionStorage.getItem('operatorCode') || !opDetails.operatorName)) {
                const opResult = await buscarInfoOperador(inputOpCode);
                if (opResult.error) { showMessage(`Operador: ${opResult.error}`, 'error', msgArea); proceed = false; } else { opDetails = opResult; }
            }
            if (proceed && inputEqCode && (inputEqCode !== sessionStorage.getItem('equipmentCode') || !eqDetails.equipmentName)) {
                const eqResult = await buscarInfoEquipamento(inputEqCode);
                if (eqResult.error) { showMessage(`Equipamento: ${eqResult.error}`, 'error', msgArea); proceed = false; } else { eqDetails = eqResult; }
            }
            if(submitBtn) submitBtn.disabled = false;
            if (proceed) {
                if(inputOpCode) { sessionStorage.setItem('operatorCode', inputOpCode); sessionStorage.setItem('operatorName', opDetails.operatorName); if(opDetails.data) sessionStorage.setItem('operatorData', JSON.stringify(opDetails.data)); }
                if(inputEqCode) { sessionStorage.setItem('equipmentCode', inputEqCode); sessionStorage.setItem('equipmentName', eqDetails.equipmentName); if(eqDetails.data) sessionStorage.setItem('equipmentData', JSON.stringify(eqDetails.data)); }
                sessionStorage.setItem('loginType', 'station');
                loadUserInfo(); closeModal(opEqModal);
                showMessage('Dados atualizados com sucesso!', 'success', mainMessageArea);
                if (currentOrderCodeForProcessing) {
                    const finalOpCode = sessionStorage.getItem('operatorCode'), finalEqCode = sessionStorage.getItem('equipmentCode');
                    if (finalOpCode && finalEqCode) { await fetchOrderStepsForDisplay(currentOrderCodeForProcessing, finalOpCode, finalEqCode); }
                }
            }
            if (!proceed || !currentOrderCodeForProcessing) { currentOrderCodeForProcessing = null; }
        });
    }

    if (ongoingTasksContainer) {
        ongoingTasksContainer.addEventListener('click', async (event) => {
            const targetButton = event.target.closest('button.btn-action-card');
            if (!targetButton || targetButton.disabled) return;
            const card = targetButton.closest('.task-card');
            if (!card) return;
            const activityId = card.dataset.activityId;
            if (targetButton.classList.contains('action-stop')) {
                const modal = document.getElementById('stopReasonModal');
                if(modal) { modal.querySelector('#stopModalActivityId').value = activityId; }
                await loadReasonsToSelect('stop'); openModal(modal);
            } else if (targetButton.classList.contains('action-nc')) {
                const modal = document.getElementById('ncModal');
                if(modal) { modal.querySelector('#ncModalActivityId').value = activityId; modal.querySelector('#ncQuantityInput').value = ''; }
                await loadReasonsToSelect('nc'); openModal(modal);
            } else if (targetButton.classList.contains('action-finish')) {
                const modal = document.getElementById('finalizeTaskModal');
                if(modal) { modal.querySelector('#finalizeModalActivityId').value = activityId; modal.querySelector('#finalizeQuantityInput').value = ''; }
                openModal(modal);
            } else if (targetButton.classList.contains('action-resume')) {
                targetButton.disabled = true; targetButton.innerHTML = `<i class="fas fa-spinner fa-spin fa-xl"></i>`;
                await resumeActivity(activityId);
            }
        });
    }

    const submitStopReasonButton = document.getElementById('submitStopReason');
    const submitFinalizeTaskButton = document.getElementById('submitFinalizeTask');
    const submitNcButton = document.getElementById('submitNc');

    if (submitStopReasonButton) submitStopReasonButton.addEventListener('click', async () => {
        const submitButton = submitStopReasonButton;
        const activityId = document.getElementById('stopModalActivityId').value;
        const reasonId = document.getElementById('stopReasonSelect').value;
        const modalMsgArea = document.getElementById('stopReasonModalMessageArea');
        if (!reasonId) { showMessage('Selecione um motivo.', 'error', modalMsgArea); return; }
        if (submitButton) submitButton.disabled = true;
        await stopActivity(activityId, reasonId);
        if (submitButton) submitButton.disabled = false;
    });
    if (submitFinalizeTaskButton) submitFinalizeTaskButton.addEventListener('click', async () => {
        const activityId = document.getElementById('finalizeModalActivityId').value;
        const quantity = document.getElementById('finalizeQuantityInput').value;
        const submitButton = submitFinalizeTaskButton;
        const modalMsgArea = document.getElementById('finalizeTaskModalMessageArea');
        if (!quantity || parseFloat(quantity) < 0) { showMessage('Insira uma quantidade válida.', 'error', modalMsgArea); return; }
        if (submitButton) submitButton.disabled = true;
        await finalizeActivityAppointment(activityId, quantity);
        if (submitButton) submitButton.disabled = false;
    });
    if (submitNcButton) submitNcButton.addEventListener('click', async () => {
        const activityId = document.getElementById('ncModalActivityId').value;
        const reasonId = document.getElementById('ncReasonSelect').value;
        const quantity = document.getElementById('ncQuantityInput').value;
        const modalMsgArea = document.getElementById('ncModalMessageArea');
        if (!reasonId) { showMessage('Selecione um motivo para NC.', 'error', modalMsgArea); return; }
        if (!quantity || parseInt(quantity, 10) <= 0) { showMessage('Insira uma quantidade NC válida.', 'error', modalMsgArea); return; }
        const submitButton = submitNcButton;
        if (submitButton) submitButton.disabled = true;
        showMessage('Registrando NC...', 'info', modalMsgArea);
        const payload = { order_activity: activityId, non_conformance: reasonId, quantity: quantity };
        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/activity-non-conformance-log/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || errorData.error || 'Falha ao registrar NC.');
            }
            showMessage('NC registrada com sucesso.', 'success', mainMessageArea);
            closeModal(document.getElementById('ncModal'));
            await fetchOngoingTasks();
        } catch (error) {
            console.error('Erro ao registrar NC:', error);
            showMessage(`Erro: ${error.message}`, 'error', modalMsgArea);
        } finally {
            if (submitButton) submitButton.disabled = false;
        }
    });

    // --- INICIALIZAÇÃO FINAL ---
    loadUserInfo();
    fetchOngoingTasks();
});