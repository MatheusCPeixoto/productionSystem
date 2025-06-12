// ../script/home.js

// A estrutura inteira fica dentro deste listener para garantir que o HTML já existe.
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
    const opForm = document.getElementById('opEqForm');

    // Modais (para fácil referência no event listener)
    const stopReasonModal = document.getElementById('stopReasonModal');
    const finalizeTaskModal = document.getElementById('finalizeTaskModal');
    const ncModal = document.getElementById('ncModal');
    const opEqModal = document.getElementById('opEqModal');
    const orderInteractionModal = document.getElementById('orderInteractionModal');


    // --- VARIÁVEIS DE ESTADO ---
    let fetchedTasksCache = [];
    let currentOrderCodeForProcessing = null;

    // --- FUNÇÕES AUXILIARES, DE BUSCA E UI ---

    function showMessage(text, type = 'info', area = mainMessageArea) {
        if (!area) { console.warn("Área de mensagem não definida:", text); alert(text); return; }
        area.textContent = text;
        // Resetando classes para garantir que apenas as corretas sejam aplicadas
        area.className = 'p-3 my-2 rounded-md text-center text-sm'; // Base classes
        // Adicionando classes de visibilidade e transição do HTML original
        area.classList.add('min-h-[2.75rem]', 'transition-opacity', 'duration-300');


        if (type === 'success') area.classList.add('message-type-success');
        else if (type === 'error') area.classList.add('message-type-error');
        else area.classList.add('message-type-info');

        if (text) {
            area.style.visibility = 'visible';
            area.style.opacity = '1';
            area.classList.add('visible'); // Adiciona a classe 'visible' definida no CSS
        } else {
            area.style.visibility = 'hidden';
            area.style.opacity = '0';
            area.classList.remove('visible'); // Remove a classe 'visible'
        }

        const isMainMsg = area === mainMessageArea;
        // A lógica de timeout para esconder a mensagem
        if (text && (type !== 'error' || isMainMsg)) {
             setTimeout(() => {
                area.style.opacity = '0';
                // Espera a transição de opacidade terminar antes de esconder
                setTimeout(() => {
                    area.style.visibility = 'hidden';
                    area.classList.remove('visible');
                    // Limpa o texto apenas se for a área principal para evitar que mensagens de erro em modais sumam rápido demais
                    if (isMainMsg) area.textContent = '';
                }, 300);
            }, isMainMsg ? 5000 : 4000);
        }
    }

    function openModal(modal) { if (modal) modal.classList.add('active'); }
    function closeModal(modal) { if (modal) modal.classList.remove('active'); }

    async function buscarInfoOperador(operatorCode) {
        const apiUrl = `http://127.0.0.1:8000/api/v1/workforce/${encodeURIComponent(operatorCode)}/`;
        try {
            const response = await fetch(apiUrl);
            if (!response.ok) { throw new Error(`Operador não encontrado (HTTP ${response.status})`); }
            const apiData = await response.json();
            if (apiData.erro) { throw new Error(apiData.erro); }
            if (apiData.hasOwnProperty('name')) { return { operatorName: apiData.name, data: apiData }; }
            throw new Error("Formato de dados do operador inesperado.");
        } catch (error) { console.error('Erro (Operador):', error); return { error: error.message, code: operatorCode }; }
    }

    async function buscarInfoEquipamento(equipmentCode) {
        const apiUrl = `http://127.0.0.1:8000/api/v1/equipments/${encodeURIComponent(equipmentCode)}/`;
        try {
            const response = await fetch(apiUrl);
            if (!response.ok) { throw new Error(`Equipamento não encontrado (HTTP ${response.status})`); }
            const apiData = await response.json();
            if (apiData.erro) { throw new Error(apiData.erro); }
            if (apiData.hasOwnProperty('description')) { return { equipmentName: apiData.description, data: apiData }; }
            throw new Error("Formato de dados do equipamento inesperado.");
        } catch (error) { console.error('Erro (Equipamento):', error); return { error: error.message, code: equipmentCode }; }
    }

    async function loadReasonsToSelect(reasonType) {
        let apiUrl = '', selectElement, modalMessageAreaElement;
        if (reasonType === 'stop') {
            apiUrl = 'http://127.0.0.1:8000/api/v1/stop-reason/?is_active=1';
            selectElement = document.getElementById('stopReasonSelect');
            modalMessageAreaElement = document.getElementById('stopReasonModalMessageArea');
        } else if (reasonType === 'nc') {
            apiUrl = 'http://127.0.0.1:8000/api/v1/non-conformance/?is_active=1';
            selectElement = document.getElementById('ncReasonSelect');
            modalMessageAreaElement = document.getElementById('ncModalMessageArea');
        } else { return; }

        if (!selectElement || !modalMessageAreaElement) {
            console.warn(`Elemento select ou área de mensagem não encontrado para ${reasonType}`);
            return;
        }
        showMessage('Carregando motivos...', 'info', modalMessageAreaElement);
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
            showMessage('', 'info', modalMessageAreaElement); // Limpa a mensagem de carregando
        } catch (error) {
            console.error(`Erro ao carregar motivos de ${apiUrl}:`, error);
            showMessage('Falha ao carregar motivos.', 'error', modalMessageAreaElement);
            selectElement.innerHTML = '<option value="">Erro ao carregar</option>';
        }
    }

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
            // Habilita multi-ordem apenas se ambos operador e equipamento estiverem definidos no modo estação
            if (operatorCode && equipmentCode) { enableMultiOrder = true; }
        }

        if (userInfoDisplay) userInfoDisplay.textContent = displayText;
        if (switchModeButtonText) switchModeButtonText.textContent = switchButtonText;
        if (changeOpEqButton) changeOpEqButton.style.display = showChangeOpEq ? 'flex' : 'none';

        const multiOrderToggleContainer = document.getElementById('multiOrderToggleContainer');

        if (multiOrderToggle) {
            multiOrderToggle.disabled = !enableMultiOrder;
            const label = multiOrderToggle.closest('label'); // O label que é o cursor-pointer

            if (multiOrderToggleContainer) {
                 multiOrderToggleContainer.style.display = enableMultiOrder ? 'flex' : 'none';
            }

            if (label) { // Atualiza o estilo do label e do container
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
            } else if (fetchedTasksCache.length === 0 && mainMessageArea.textContent.includes('Buscando')) {
                showMessage('Nenhum apontamento em andamento.', 'info', mainMessageArea);
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
            tasks.forEach(task => {
                const card = createCardElement(task);
                ongoingTasksContainer.appendChild(card);
            });
        } else {
            noOngoingTasksMessage.textContent = "Nenhum apontamento em andamento.";
            noOngoingTasksMessage.classList.remove('hidden');
        }
        filterOngoingTasks();
    }

    function createCardElement(task) {
        const operatorNames = (task.active_workforce_log || []).map(log => log.workforce_name || 'N/D');
        const equipmentNames = (task.active_equipment_log || []).map(log => log.equipment_description || 'N/D');
        const card = document.createElement('div');
        card.className = 'bg-industrial-medium p-5 rounded-xl shadow-lg task-card flex flex-col justify-between border border-industrial-light';
        card.dataset.orderId = task.order_code;
        card.dataset.activityId = task.code; // ID do OrderActivityProgress
        const status = task.status || 'Desconhecido';
        card.dataset.status = status.toLowerCase();
        card.dataset.searchableContent = `${task.order_code} ${task.activity?.description} ${operatorNames.join(' ')} ${equipmentNames.join(' ')}`.toLowerCase();

        let statusVisualClass = '';
        // A classe status-parado-blinking é aplicada diretamente no HTML se o status for 'Parado'
        if (status === 'Em Andamento') { statusVisualClass = 'bg-green-500 text-white'; }
        else if (status === 'Parado') { statusVisualClass = 'bg-yellow-500 text-white status-parado-blinking'; }
        else if (status === 'Finalizado') { statusVisualClass = 'bg-blue-500 text-white'; }
        else { statusVisualClass = 'bg-gray-500 text-white'; }

        card.innerHTML = `
            <div class="flex-grow">
                <div class="mb-4 text-center"><span class="px-3 py-1 inline-flex text-sm leading-tight font-bold rounded-full ${statusVisualClass}">${status}</span></div>
                <div class="mb-3"><p class="text-industrial-primary text-lg font-bold truncate" title="${task.activity?.description || 'N/A'}">${task.activity?.description || 'Atividade não informada'}</p><p class="text-industrial-secondary text-sm" title="Ordem: ${task.order_code}"><strong class="font-semibold">OP:</strong> ${task.order_code} | <strong class="font-semibold">Seq:</strong> ${task.sequence}</p></div>
                <div class="mb-4 text-sm text-industrial-secondary"><p><i class="fas fa-calendar-alt mr-2 w-4 text-center"></i>Iniciado em: ${task.start_date ? new Date(task.start_date).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }) : '-'}</p></div>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 border-t border-b border-industrial-light py-3 my-3">
                    <div><h4 class="font-semibold text-industrial-secondary text-xs uppercase mb-1"><i class="fas fa-users-cog mr-1"></i> Operadores</h4><ul class="text-industrial-primary text-sm space-y-1">${operatorNames.length > 0 ? operatorNames.map(name => `<li class="truncate" title="${name}">${name}</li>`).join('') : '<li>-</li>'}</ul></div>
                    <div><h4 class="font-semibold text-industrial-secondary text-xs uppercase mb-1"><i class="fas fa-cogs mr-1"></i> Equipamentos</h4><ul class="text-industrial-primary text-sm space-y-1">${equipmentNames.length > 0 ? equipmentNames.map(name => `<li class="truncate" title="${name}">${name}</li>`).join('') : '<li>-</li>'}</ul></div>
                </div>
            </div>
            <div class="mt-auto flex flex-wrap justify-around gap-4 pt-4 border-t border-industrial-light">
                <button title="Retomar" data-action="resume-task" class="btn-action-card bg-industrial-light text-blue-400 hover:bg-blue-500 hover:text-white p-3 rounded-lg flex items-center justify-center w-12 h-12 ${status !== 'Parado' ? 'opacity-50 cursor-not-allowed' : ''}" ${status !== 'Parado' ? 'disabled' : ''}><i class="fas fa-play-circle fa-xl"></i></button>
                <button title="Parada" data-action="stop-task" class="btn-action-card bg-industrial-light text-yellow-400 hover:bg-yellow-500 hover:text-white p-3 rounded-lg flex items-center justify-center w-12 h-12 ${status !== 'Em Andamento' ? 'opacity-50 cursor-not-allowed' : ''}" ${status !== 'Em Andamento' ? 'disabled' : ''}><i class="fas fa-pause-circle fa-xl"></i></button>
                <button title="Finalizar" data-action="finish-task" class="btn-action-card bg-industrial-light text-green-400 hover:bg-green-500 hover:text-white p-3 rounded-lg flex items-center justify-center w-12 h-12 ${status === 'Finalizado' ? 'opacity-50 cursor-not-allowed' : ''}" ${status === 'Finalizado' ? 'disabled' : ''}><i class="fas fa-check-circle fa-xl"></i></button>
                <button title="Não Conformidade" data-action="nc-task" class="btn-action-card bg-industrial-light text-red-400 hover:bg-red-500 hover:text-white p-3 rounded-lg flex items-center justify-center w-12 h-12"><i class="fas fa-exclamation-triangle fa-xl"></i></button>
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

        const hasTasksInCache = fetchedTasksCache.length > 0;
        if (visibleCardsCount === 0) {
            noOngoingTasksMessage.classList.remove('hidden');
            if (hasTasksInCache && searchTerm) {
                noOngoingTasksMessage.textContent = "Nenhum apontamento encontrado para o termo pesquisado.";
            } else if (!hasTasksInCache) {
                noOngoingTasksMessage.textContent = "Nenhum apontamento em andamento.";
            } else { // Tem tarefas no cache, mas o filtro não achou nada (e não tem termo de busca, o que é estranho, mas cobre)
                 noOngoingTasksMessage.textContent = "Nenhum apontamento em andamento visível.";
            }
        } else {
            noOngoingTasksMessage.classList.add('hidden');
        }
    }

    async function handleMultiOrderStop(activityIdToExclude = null) {
        const isMultiOrderMode = sessionStorage.getItem('multiOrderModeEnabled') === 'true';
        if (!isMultiOrderMode) return true; // Se não está no modo, permite prosseguir

        // Encontra a tarefa que está "Em Andamento" e não é a que estamos tentando manipular (activityIdToExclude)
        const activeTask = fetchedTasksCache.find(task =>
            task.status === 'Em Andamento' &&
            (!activityIdToExclude || task.code.toString() !== activityIdToExclude.toString())
        );

        if (activeTask) {
            showMessage(`Modo Múltipla Ordem: Parando automaticamente a tarefa ${activeTask.order_code} / ${activeTask.activity.description} (ID: ${activeTask.code})...`, 'info', mainMessageArea);
            // Usa um motivo de parada padrão para paradas automáticas (ex: '20' - Parada Automática Sistema)
            // O 'false' é para não mostrar mensagem de sucesso da parada automática na área principal,
            // pois a mensagem principal será da ação que o usuário está realizando.
            const stopResult = await stopActivity(activeTask.code, '20', false);
            if (!stopResult.success) {
                showMessage(`Falha ao parar automaticamente a tarefa anterior (${activeTask.code}). Ação cancelada.`, 'error', mainMessageArea);
                await fetchOngoingTasks(); // Atualiza para refletir o estado real
                return false; // Impede a ação original
            }
            // Não precisa de 'else', se deu certo, a função continua e retorna true no final.
        }
        return true; // Permite prosseguir se não havia tarefa para parar ou se a parada foi bem-sucedida
    }


    async function stopActivity(activityId, reasonId, showSuccessMsg = true) {
        const apiUrl = `http://127.0.0.1:8000/api/v1/order-activity-progress/${activityId}/stop/`;
        const modalMsgArea = stopReasonModal ? stopReasonModal.querySelector('#stopReasonModalMessageArea') : mainMessageArea;

        if (!reasonId) {
            showMessage('Por favor, selecione um motivo para a parada.', 'error', modalMsgArea);
            return { success: false, error: 'Motivo não selecionado' };
        }

        if(showSuccessMsg) showMessage(`Registrando parada para atividade ${activityId}...`, 'info', modalMsgArea);

        try {
            const payload = { stop_reason_code: reasonId };
            // Adiciona multi_order_mode ao payload se necessário pela lógica do backend ao parar
            // payload.multi_order_mode = sessionStorage.getItem('multiOrderModeEnabled') === 'true';

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Falha ao registrar parada (HTTP ${response.status})`);
            }
            const result = await response.json();
            if (showSuccessMsg) {
                showMessage(result.message || `Atividade ${activityId} parada.`, 'success', mainMessageArea);
            }
            if(stopReasonModal) closeModal(stopReasonModal);
            await fetchOngoingTasks(); // Atualiza a lista após a ação
            return { success: true };
        } catch (error) {
            console.error("Erro ao parar atividade:", error);
            showMessage(`Erro: ${error.message}`, 'error', modalMsgArea);
            // Não recarrega as tarefas aqui, pois pode ter sido uma falha de validação (ex: motivo não selecionado)
            return { success: false, error: error.message };
        }
    }

    async function resumeActivity(activityIdToResume) {
        // Verifica se outra tarefa precisa ser parada antes de retomar esta
        const canProceed = await handleMultiOrderStop(activityIdToResume);
        if (!canProceed) {
            await fetchOngoingTasks(); // Garante que a UI reflita o estado atual se a ação foi bloqueada
            return;
        }

        const apiUrl = `http://127.0.0.1:8000/api/v1/order-activity-progress/${activityIdToResume}/resume/`;
        showMessage(`Retomando apontamento ${activityIdToResume}...`, 'info', mainMessageArea);

        try {
            const payload = {
                multi_order_mode: sessionStorage.getItem('multiOrderModeEnabled') === 'true'
            };
            const response = await fetch(apiUrl, {
                 method: 'POST',
                 headers: { 'Content-Type': 'application/json' }, // Adicionado para consistência, mesmo que o corpo seja simples
                 body: JSON.stringify(payload) // Envia o payload
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Falha ao retomar (HTTP ${response.status})`);
            }
            const result = await response.json();
            showMessage(result.message || `Apontamento ${activityIdToResume} retomado!`, 'success', mainMessageArea);
            await fetchOngoingTasks();
        } catch (error) {
            console.error("Erro ao retomar atividade:", error);
            showMessage(`Erro ao retomar: ${error.message}`, 'error', mainMessageArea);
            await fetchOngoingTasks(); // Atualiza para refletir o estado real, mesmo em caso de erro
        }
    }

    async function finalizeActivityAppointment(activityId, quantity) {
        const modalMsgArea = finalizeTaskModal ? finalizeTaskModal.querySelector('#finalizeTaskModalMessageArea') : mainMessageArea;
        if (!quantity || parseFloat(quantity) < 0) {
            showMessage('Insira uma quantidade produzida válida (maior ou igual a zero).', 'error', modalMsgArea);
            return;
        }
        showMessage('Finalizando apontamento...', 'info', modalMsgArea);

        const apiUrl = `http://127.0.0.1:8000/api/v1/order-activity-progress/${activityId}/`;
        try {
            const response = await fetch(apiUrl, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ quantity: parseFloat(quantity) })
            });
            if (!response.ok) {
                const err = await response.json();
                throw new Error(`Falha ao finalizar: ${err.error || JSON.stringify(err)} (HTTP ${response.status})`);
            }
            const result = await response.json();
            showMessage(result.message || 'Apontamento finalizado com sucesso!', 'success', mainMessageArea);
            if(finalizeTaskModal) closeModal(finalizeTaskModal);
            await fetchOngoingTasks();
        } catch (error) {
            console.error("Erro ao finalizar apontamento:", error);
            showMessage(`Erro: ${error.message}`, 'error', modalMsgArea);
        }
    }

    async function startActivityAppointment(stepInfo, tempOperatorCode, tempEquipmentCode) {
        const modalMsgArea = orderInteractionModal ? orderInteractionModal.querySelector('#orderInteractionModalMessageArea') : mainMessageArea;
        const failedButton = document.querySelector(`button[data-step-info*='"code":${stepInfo.code}']`);

        // Verifica se outra tarefa precisa ser parada antes de iniciar esta
        const canProceed = await handleMultiOrderStop(); // Não passa ID para excluir, pois é uma nova tarefa
        if (!canProceed) {
            if (failedButton) {
                failedButton.disabled = false;
                const spinner = failedButton.querySelector('i.fa-spinner');
                if (spinner) spinner.remove();
            }
            // A mensagem de erro já foi mostrada por handleMultiOrderStop
            return;
        }

        const operatorCode = tempOperatorCode || sessionStorage.getItem('operatorCode');
        const equipmentCode = tempEquipmentCode || sessionStorage.getItem('equipmentCode');

        if (!operatorCode || !equipmentCode) {
            showMessage('Operador ou Equipamento não definido. Verifique as configurações.', 'error', modalMsgArea);
             if (failedButton) {
                failedButton.disabled = false;
                const spinner = failedButton.querySelector('i.fa-spinner');
                if (spinner) spinner.remove();
            }
            return;
        }

        showMessage('Iniciando apontamento...', 'info', modalMsgArea);
        const payload = {
            company_code: stepInfo.company_code,
            branch_code: stepInfo.branch_code,
            order_code: stepInfo.order_code,
            activity_code: stepInfo.activity_code, // Este é o código da Atividade (ex: 'TORNO-01')
            sequence: stepInfo.sequence,
            operator_code: operatorCode,
            equipment_code: equipmentCode,
            multi_order_mode: sessionStorage.getItem('multiOrderModeEnabled') === 'true'
        };

        try {
            const apiUrl = `http://127.0.0.1:8000/api/v1/order-activity-progress/start/`;
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Falha ao iniciar apontamento: ${errorData.error || JSON.stringify(errorData)} (HTTP ${response.status})`);
            }
            const result = await response.json();
            showMessage(result.message || 'Apontamento iniciado com sucesso!', 'success', mainMessageArea);
            if(orderInteractionModal) closeModal(orderInteractionModal);
            await fetchOngoingTasks();
        } catch (error) {
            console.error("Erro ao iniciar apontamento:", error);
            showMessage(`Erro: ${error.message}`, 'error', modalMsgArea);
            if (failedButton) {
                failedButton.disabled = false;
                const spinner = failedButton.querySelector('i.fa-spinner');
                if (spinner) spinner.remove();
            }
        }
    }

    function openOpEqModalForChanges(requireOperator, requireEquipment, clearInputsIfTerminalOrderContext = false) {
        if (!opEqModal) return;
        const opInput = opEqModal.querySelector('#modalOperatorCode');
        const eqInput = opEqModal.querySelector('#modalEquipmentCode');
        const opGroup = opEqModal.querySelector('#operatorInputGroup');
        const eqGroup = opEqModal.querySelector('#equipmentInputGroup');
        const msgArea = opEqModal.querySelector('#opEqModalMessageArea');

        if (opGroup) opGroup.style.display = 'block';
        if (opInput) {
            // Limpa o campo se for contexto de abrir ordem no modo terminal
            opInput.value = clearInputsIfTerminalOrderContext ? '' : (sessionStorage.getItem('operatorCode') || '');
            opInput.required = requireOperator;
        }

        if (eqGroup) eqGroup.style.display = 'block';
        if (eqInput) {
            // Limpa o campo se for contexto de abrir ordem no modo terminal
            eqInput.value = clearInputsIfTerminalOrderContext ? '' : (sessionStorage.getItem('equipmentCode') || '');
            eqInput.required = requireEquipment;
        }

        let messageText = 'Insira os códigos necessários.';
        if (requireOperator && requireEquipment) messageText = 'Operador e Equipamento são obrigatórios.';
        else if (requireOperator) messageText = 'Código do Operador é obrigatório.';
        else if (requireEquipment) messageText = 'Código do Equipamento é obrigatório.';

        showMessage(messageText, 'info', msgArea);
        openModal(opEqModal);
    }

    async function fetchOrderStepsForDisplay(orderCode, operatorCode, equipmentCode) {
        if (!orderInteractionModal) return;
        const modalTitle = orderInteractionModal.querySelector('#orderInteractionModalTitle');
        const modalContent = orderInteractionModal.querySelector('#orderInteractionModalContent');
        const modalMsgArea = orderInteractionModal.querySelector('#orderInteractionModalMessageArea');

        const apiUrl = `http://127.0.0.1:8000/api/v1/order-items/?order_code=${encodeURIComponent(orderCode)}`;

        if(modalTitle) modalTitle.textContent = `Etapas da Ordem: ${orderCode}`;
        if(modalContent) modalContent.innerHTML = `<p class="text-industrial-secondary p-4 text-center">Buscando etapas...</p>`;
        showMessage('', 'info', modalMsgArea); // Limpa mensagens anteriores
        openModal(orderInteractionModal);

        try {
            const response = await fetch(apiUrl);
            if (!response.ok) throw new Error(`Erro ao buscar etapas: ${response.statusText} (HTTP ${response.status})`);
            const orderItems = await response.json();

            // Assume que orderItems é uma lista de itens de pedido, cada um podendo ter 'structure_activities'
            const allSteps = Array.isArray(orderItems) ? orderItems.flatMap(item =>
                (item.structure_activities || []).map(activity => ({
                    ...activity, // Contém activity_code, activity_description, sequence
                    order_code: item.order_code, // Adiciona o código da ordem ao objeto da etapa
                    company_code: item.company_code, // Adiciona company_code
                    branch_code: item.branch_code   // Adiciona branch_code
                }))
            ) : [];

            if (allSteps.length > 0) {
                if(modalContent) modalContent.innerHTML = `
                    <p class="text-sm text-industrial-secondary mb-3">Selecione a etapa para iniciar:</p>
                    <div class="space-y-2 max-h-60 overflow-y-auto">
                        ${allSteps.map(step => `
                            <button
                                data-step-info='${JSON.stringify(step)}'
                                class="w-full text-left p-3 bg-industrial-dark hover:bg-industrial-light rounded-md order-step-button text-industrial-primary">
                                <strong>${step.activity_description || 'Descrição não disponível'}</strong>
                                <span class="text-xs text-industrial-secondary">(Seq: ${step.sequence})</span>
                            </button>
                        `).join('')}
                    </div>`;

                // Adiciona event listeners aos botões de etapa recém-criados
                modalContent.querySelectorAll('.order-step-button').forEach(button => {
                    button.onclick = async () => {
                        const stepInfo = JSON.parse(button.dataset.stepInfo);
                        button.disabled = true;
                        button.innerHTML += ' <i class="fas fa-spinner fa-spin ml-2"></i>';
                        // Passa operatorCode e equipmentCode que já foram validados ou obtidos
                        await startActivityAppointment(stepInfo, operatorCode, equipmentCode);
                    };
                });
            } else {
                if(modalContent) modalContent.innerHTML = `<p class="text-red-400 p-4 text-center">Nenhuma etapa de roteiro encontrada para esta ordem ou item.</p>`;
            }
        } catch (error) {
            console.error('Erro ao buscar etapas da ordem:', error);
            if(modalContent) modalContent.innerHTML = `<p class="text-red-400 p-4 text-center">Falha ao carregar etapas. ${error.message}</p>`;
            if(modalMsgArea) showMessage('Falha ao carregar etapas.', 'error', modalMsgArea);
        }
    }

    async function validateLoginModeAndProceed(orderCode) {
        const loginType = sessionStorage.getItem('loginType');
        let opCode = sessionStorage.getItem('operatorCode');
        let eqCode = sessionStorage.getItem('equipmentCode');

        let needsOp = !opCode;
        let needsEq = !eqCode;
        let clearInputsForModal = false; // Flag para limpar inputs no modal Op/Eq

        if (loginType === 'terminal') { // Em modo terminal, sempre precisa informar e limpar os campos
            needsOp = true;
            needsEq = true;
            clearInputsForModal = true;
        }
        // Se já estiver em modo 'station', mas faltar algum, também precisa (clearInputsForModal será false)

        if (needsOp || needsEq) {
            // Guarda o código da ordem para processar depois que op/eq forem informados
            currentOrderCodeForProcessing = orderCode;
            openOpEqModalForChanges(needsOp, needsEq, clearInputsForModal); // Passa a flag
        } else {
            // Já tem op e eq (provavelmente modo estação ou terminal já configurado anteriormente - este último caso não deveria acontecer com a nova lógica)
            await fetchOrderStepsForDisplay(orderCode, opCode, eqCode);
        }
    }

    function displayOrderCodeInputInModal() {
        if (!orderInteractionModal) return;
        const modalTitle = orderInteractionModal.querySelector('#orderInteractionModalTitle');
        const modalContent = orderInteractionModal.querySelector('#orderInteractionModalContent');
        const modalMsgArea = orderInteractionModal.querySelector('#orderInteractionModalMessageArea');

        if(modalTitle) modalTitle.textContent = 'Abrir Ordem de Produção';
        if(modalContent) modalContent.innerHTML = `
            <form id="modalOrderCodeForm" class="space-y-4">
                <div>
                    <label for="modalOrderCode" class="block text-sm font-medium text-white mb-1">Código da Ordem:</label>
                    <input type="text" id="modalOrderCode" class="w-full p-2 border-2 border-industrial-light bg-industrial-dark text-white rounded-md" required>
                </div>
                <button type="submit" class="w-full bg-industrial-accent hover:bg-sky-400 text-white font-semibold py-2 px-4 rounded-md">Buscar Etapas</button>
            </form>`;
        if(modalMsgArea) showMessage('', 'info', modalMsgArea); // Limpa mensagens anteriores

        openModal(orderInteractionModal);

        const form = document.getElementById('modalOrderCodeForm');
        if (form) {
            form.onsubmit = async (e) => {
                e.preventDefault();
                const orderCodeInput = document.getElementById('modalOrderCode');
                const orderCode = orderCodeInput ? orderCodeInput.value.trim() : null;
                if (orderCode) {
                    // currentOrderCodeForProcessing = orderCode; // Definido dentro de validateLoginModeAndProceed se necessário
                    await validateLoginModeAndProceed(orderCode);
                } else {
                    if(modalMsgArea) showMessage('Insira um código de ordem válido.', 'error', modalMsgArea);
                }
            };
        }
    }

    // --- EVENT LISTENERS E INICIALIZAÇÃO ---
    function setupEventListeners() {
        // Listener para cliques no body (para botões de ação, modais, etc.)
        document.body.addEventListener('click', async (event) => {
            const button = event.target.closest('button');
            if (!button || button.disabled) return; // Ignora se não for um botão ou se estiver desabilitado

            const action = button.dataset.action; // Pega o data-action do botão clicado
            const card = button.closest('.task-card');
            const modal = button.closest('.modal');

            // Tenta pegar o activityId do card se a ação for em um card, ou do input hidden no modal
            let activityId = card ? card.dataset.activityId : null;
            if (!activityId && modal) {
                const activityIdInput = modal.querySelector('[id$="ModalActivityId"]'); // Ex: stopModalActivityId
                if (activityIdInput) activityId = activityIdInput.value;
            }

            // Ações do Cabeçalho (identificadas por ID)
            if (button.id === 'triggerOpenOrderModalButton') {
                currentOrderCodeForProcessing = null; // Reseta para nova busca de ordem
                displayOrderCodeInputInModal();
                return;
            }
            if (button.id === 'changeOpEqButton') {
                currentOrderCodeForProcessing = null; // Não está processando uma ordem específica ao trocar op/eq globalmente
                openOpEqModalForChanges(true, true); // Requer ambos para modo estação
                return;
            }
            if (button.id === 'switchModeButton') {
                const currentLoginType = sessionStorage.getItem('loginType');
                currentOrderCodeForProcessing = null; // Reseta ao trocar de modo
                if (currentLoginType === 'station') {
                    sessionStorage.setItem('loginType', 'terminal');
                    // Limpa dados específicos do modo estação
                    ['operatorCode', 'operatorName', 'operatorData', 'equipmentCode', 'equipmentName', 'equipmentData', 'multiOrderModeEnabled'].forEach(item => sessionStorage.removeItem(item));
                    loadUserInfo(); // Atualiza a UI (inclusive o toggle de multi-ordem)
                    showMessage('Modo alterado para Terminal. Multi-Ordem desativado.', 'success', mainMessageArea);
                } else { // Estava em terminal, quer ir para estação
                    showMessage('Para ativar o Modo Estação, por favor, informe o Operador e o Equipamento.', 'info', mainMessageArea);
                    openOpEqModalForChanges(true, true); // Requer ambos para modo estação
                }
                return;
            }

            // Ações baseadas em data-action
            if (action) {
                switch (action) {
                    // Ações nos Cartões
                    case 'resume-task':
                        button.disabled = true; button.innerHTML = `<i class="fas fa-spinner fa-spin fa-xl"></i>`;
                        await resumeActivity(activityId);
                        // O botão será re-renderizado ou seu estado atualizado por fetchOngoingTasks
                        break;
                    case 'stop-task':
                        if (stopReasonModal && activityId) {
                            stopReasonModal.querySelector('#stopModalActivityId').value = activityId;
                            await loadReasonsToSelect('stop');
                            openModal(stopReasonModal);
                        }
                        break;
                    case 'finish-task':
                        if (finalizeTaskModal && activityId) {
                            finalizeTaskModal.querySelector('#finalizeModalActivityId').value = activityId;
                            const qtyInput = finalizeTaskModal.querySelector('#finalizeQuantityInput');
                            if(qtyInput) qtyInput.value = ''; // Limpa valor anterior
                            showMessage('', 'info', finalizeTaskModal.querySelector('#finalizeTaskModalMessageArea')); // Limpa msg anterior
                            openModal(finalizeTaskModal);
                        }
                        break;
                    case 'nc-task':
                        if (ncModal && activityId) {
                            ncModal.querySelector('#ncModalActivityId').value = activityId;
                            const qtyNcInput = ncModal.querySelector('#ncQuantityInput');
                            if(qtyNcInput) qtyNcInput.value = ''; // Limpa valor anterior
                            showMessage('', 'info', ncModal.querySelector('#ncModalMessageArea')); // Limpa msg anterior
                            await loadReasonsToSelect('nc');
                            openModal(ncModal);
                        }
                        break;

                    // Submits de Modais e outras ações (exceto opEqForm que é tratado separadamente abaixo)
                    case 'submit-stop': // ID do botão no HTML: submitStopReason
                        if (modal && modal.id === 'stopReasonModal') {
                            button.disabled = true;
                            const reasonId = modal.querySelector('#stopReasonSelect').value;
                            const currentActivityId = modal.querySelector('#stopModalActivityId').value;
                            await stopActivity(currentActivityId, reasonId);
                            button.disabled = false;
                        }
                        break;
                    case 'submit-finalize': // ID do botão no HTML: submitFinalizeTask
                         if (modal && modal.id === 'finalizeTaskModal') {
                            button.disabled = true;
                            const quantity = modal.querySelector('#finalizeQuantityInput').value;
                            const currentActivityId = modal.querySelector('#finalizeModalActivityId').value;
                            await finalizeActivityAppointment(currentActivityId, quantity);
                            button.disabled = false; // Reabilita após a tentativa
                        }
                        break;
                    case 'submit-nc': // ID do botão no HTML: submitNc
                        if (modal && modal.id === 'ncModal') {
                            button.disabled = true;
                            const ncReasonId = modal.querySelector('#ncReasonSelect').value;
                            const ncQuantity = modal.querySelector('#ncQuantityInput').value;
                            const currentActivityId = modal.querySelector('#ncModalActivityId').value; // Certifique-se que é o activityId correto
                            const ncMsgArea = modal.querySelector('#ncModalMessageArea');

                            if (!ncReasonId) { showMessage('Selecione um motivo para a não conformidade.', 'error', ncMsgArea); button.disabled = false; return; }
                            if (!ncQuantity || parseInt(ncQuantity, 10) <= 0) { showMessage('Insira uma quantidade válida para a não conformidade.', 'error', ncMsgArea); button.disabled = false; return; }

                            showMessage('Registrando Não Conformidade...', 'info', ncMsgArea);
                            const payload = {
                                order_activity: currentActivityId, // ID do OrderActivityProgress
                                non_conformance: ncReasonId,     // ID/Código do motivo da NC
                                quantity: parseInt(ncQuantity, 10)
                            };
                            try {
                                const response = await fetch('http://127.0.0.1:8000/api/v1/activity-non-conformance-log/', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify(payload)
                                });
                                if (!response.ok) {
                                    const errData = await response.json();
                                    throw new Error(errData.detail || errData.error || `Falha ao registrar NC (HTTP ${response.status})`);
                                }
                                showMessage('Não Conformidade registrada com sucesso!', 'success', mainMessageArea);
                                closeModal(modal);
                            } catch (error) {
                                console.error('Erro ao registrar NC:', error);
                                showMessage(`Erro: ${error.message}`, 'error', ncMsgArea);
                            } finally {
                                button.disabled = false;
                            }
                        }
                        break;

                    // Botão de Fechar Modal genérico
                    case 'close-modal':
                        if (modal) {
                            closeModal(modal);
                            // Limpar mensagens de erro específicas do modal ao fechar
                            const modalMsgArea = modal.querySelector('[id$="ModalMessageArea"]');
                            if (modalMsgArea) showMessage('', 'info', modalMsgArea);
                        }
                        break;
                }
            }
        });

        // Listener para o submit do formulário opEqModal (opEqForm) - REGISTRADO UMA VEZ
        if (opForm) {
            opForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const submitBtn = opForm.querySelector('button[type="submit"]');
                const msgArea = opForm.querySelector('#opEqModalMessageArea');

                // Captura o tipo de login NO MOMENTO em que o processo que levou a este submit começou.
                const loginTypeWhenModalWasTriggered = sessionStorage.getItem('loginType');

                if(submitBtn) submitBtn.disabled = true;
                showMessage('Validando informações...', 'info', msgArea);

                const opInput = opForm.querySelector('#modalOperatorCode');
                const eqInput = opForm.querySelector('#modalEquipmentCode');

                const inputOpCode = (opInput && opInput.required) ? opInput.value.trim() : (opInput ? opInput.value.trim() : null);
                const inputEqCode = (eqInput && eqInput.required) ? eqInput.value.trim() : (eqInput ? eqInput.value.trim() : null);

                if (opInput && opInput.required && !inputOpCode) {
                    showMessage('Código do Operador é obrigatório.', 'error', msgArea);
                    if(submitBtn) submitBtn.disabled = false;
                    return;
                }
                if (eqInput && eqInput.required && !inputEqCode) {
                    showMessage('Código do Equipamento é obrigatório.', 'error', msgArea);
                    if(submitBtn) submitBtn.disabled = false;
                    return;
                }

                let opDetails = {}, eqDetails = {};
                let proceed = true;

                if (inputOpCode) {
                    const opResult = await buscarInfoOperador(inputOpCode);
                    if (opResult.error) {
                        showMessage(`Operador: ${opResult.error}`, 'error', msgArea);
                        proceed = false;
                    } else {
                        opDetails = opResult;
                    }
                }

                if (proceed && inputEqCode) {
                    const eqResult = await buscarInfoEquipamento(inputEqCode);
                    if (eqResult.error) {
                        showMessage(`Equipamento: ${eqResult.error}`, 'error', msgArea);
                        proceed = false;
                    } else {
                        eqDetails = eqResult;
                    }
                }

                if(submitBtn) submitBtn.disabled = false;

                if (proceed) {
                    // CASO 1: Estava em MODO TERMINAL e o modal Op/Eq foi aberto para uma ORDEM ESPECÍFICA.
                    // Os códigos são temporários para esta ordem. Não salva no sessionStorage, não muda o modo.
                    if (loginTypeWhenModalWasTriggered === 'terminal' && currentOrderCodeForProcessing && inputOpCode && inputEqCode) {
                        closeModal(opEqModal);
                        // Usar os códigos fornecidos (inputOpCode, inputEqCode) diretamente para buscar as etapas.
                        await fetchOrderStepsForDisplay(currentOrderCodeForProcessing, inputOpCode, inputEqCode);
                        currentOrderCodeForProcessing = null; // Limpa após o uso.
                    }
                    // CASO 2: Qualquer outra situação (configurar/atualizar Modo Estação ou voltar para Terminal).
                    else {
                        if (inputOpCode && inputEqCode) {
                            // Ambos os códigos fornecidos: configurar ou atualizar para Modo Estação.
                            sessionStorage.setItem('loginType', 'station');
                            sessionStorage.setItem('operatorCode', inputOpCode);
                            sessionStorage.setItem('operatorName', opDetails.operatorName);
                            if(opDetails.data) sessionStorage.setItem('operatorData', JSON.stringify(opDetails.data));
                            sessionStorage.setItem('equipmentCode', inputEqCode);
                            sessionStorage.setItem('equipmentName', eqDetails.equipmentName);
                            if(eqDetails.data) sessionStorage.setItem('equipmentData', JSON.stringify(eqDetails.data));

                            loadUserInfo(); // Atualiza a UI, habilita multi-ordem se aplicável.
                            showMessage('Modo Estação configurado/atualizado.', 'success', mainMessageArea);
                        } else if (loginTypeWhenModalWasTriggered === 'station') {
                            // Estava em Modo Estação, mas agora os códigos estão incompletos (um ou ambos não fornecidos/limpos).
                            // Volta para Modo Terminal.
                            sessionStorage.setItem('loginType', 'terminal');
                            ['operatorCode', 'operatorName', 'operatorData', 'equipmentCode', 'equipmentName', 'equipmentData', 'multiOrderModeEnabled'].forEach(item => sessionStorage.removeItem(item));
                            loadUserInfo();
                            showMessage('Dados de Op/Eq incompletos. Retornando ao Modo Terminal.', 'info', mainMessageArea);
                        }
                        // Se loginTypeWhenModalWasTriggered era 'terminal', não havia currentOrderCodeForProcessing,
                        // e o usuário não forneceu ambos os códigos (inputOpCode && inputEqCode é falso),
                        // o modal apenas fecha. Mensagens de erro sobre campos obrigatórios já teriam sido mostradas.

                        closeModal(opEqModal);

                        // Se havia uma ordem pendente E AGORA estamos em modo estação com dados válidos (após as operações acima).
                        if (currentOrderCodeForProcessing && sessionStorage.getItem('loginType') === 'station' && sessionStorage.getItem('operatorCode') && sessionStorage.getItem('equipmentCode')) {
                            await fetchOrderStepsForDisplay(
                                currentOrderCodeForProcessing,
                                sessionStorage.getItem('operatorCode'), // Usa do sessionStorage porque o modo é estação
                                sessionStorage.getItem('equipmentCode')
                            );
                            currentOrderCodeForProcessing = null;
                        } else if (currentOrderCodeForProcessing) {
                            // Havia uma ordem pendente, mas não foi possível configurar o modo estação ou obter os dados necessários.
                            showMessage('Operador e Equipamento são necessários para abrir a ordem. Verifique as configurações.', 'error', mainMessageArea);
                            currentOrderCodeForProcessing = null;
                        }
                    }
                }
                // Se 'proceed' for false, as mensagens de erro já foram mostradas pelas validações ou buscas.
            });
        }

        // Outros listeners
        if (searchInputOngoingTasks) {
            searchInputOngoingTasks.addEventListener('input', filterOngoingTasks);
        }
        if (multiOrderToggle) {
            multiOrderToggle.addEventListener('change', (event) => {
                const isEnabled = event.target.checked;
                sessionStorage.setItem('multiOrderModeEnabled', isEnabled);
                showMessage(`Modo Múltipla Ordem ${isEnabled ? 'ATIVADO' : 'DESATIVADO'}.`, 'info', mainMessageArea);
                // Se desativado, não há ação imediata nas tarefas existentes.
                // A lógica de parada automática só ocorre ao iniciar/retomar uma nova tarefa.
            });
        }
    }
// ../script/home.js

// ... (código existente) ...

// ../script/home.js

// ... (todo o código anterior, incluindo a PRIMEIRA E COMPLETA definição de setupEventListeners) ...

    // --- WEBSOCKET ---
    let taskWebSocket = null;

    function setupWebSocket() {
        // Use ws:// para HTTP ou wss:// para HTTPS
        const wsUrl = `ws://127.0.0.1:8000/ws/tasks/`; // Configure esta URL no seu Django Channels routing
        taskWebSocket = new WebSocket(wsUrl);

        taskWebSocket.onopen = function(e) {
            console.log('WebSocket connection opened.');
            // Opcional: enviar alguma mensagem inicial para o servidor
        };

        taskWebSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            console.log('WebSocket message received:', data);

            if (data.type === 'task_update') {
                // Uma tarefa foi atualizada no backend.
                // A forma mais simples é re-carregar todas as tarefas.
                // Uma forma mais otimizada seria atualizar apenas o card específico.
                showMessage(`Atualização recebida para tarefa ${data.activity_id}. Atualizando lista...`, 'info', mainMessageArea);
                fetchOngoingTasks(); // Re-carrega a lista completa
            }
            // Adicionar outros tipos de mensagens se necessário
        };

        taskWebSocket.onerror = function(e) {
            console.error('WebSocket error observed:', e);
            // Tentar reconectar após um tempo?
        };

        taskWebSocket.onclose = function(e) {
            console.log('WebSocket connection closed, code:', e.code, 'reason:', e.reason);
            // Tentar reconectar após um tempo se o fechamento não for intencional
            if (e.code !== 1000) { // 1000 é fechamento normal
                console.log('Attempting to reconnect WebSocket in 5 seconds...');
                setTimeout(setupWebSocket, 5000); // Tenta reconectar após 5 segundos
            }
        };
    }

    // --- INICIALIZAÇÃO DO SCRIPT ---
    // Certifique-se que a setupEventListeners() chamada aqui é a versão completa definida anteriormente.
    setupEventListeners();
    loadUserInfo();
    fetchOngoingTasks();
    setupWebSocket(); // Inicia a conexão WebSocket quando a página carrega
});