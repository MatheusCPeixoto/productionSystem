// frontend/script/order-details.js

// Função global para o modal de imagem, acessível pelo HTML
window.openImageModal = (src) => {
    const imageModal = document.getElementById('imageModal');
    const modalImageSrc = document.getElementById('modalImageSrc');
    if (modalImageSrc && imageModal) {
        modalImageSrc.src = src;
        imageModal.classList.remove('hidden');
        imageModal.classList.add('flex');
    }
};

document.addEventListener('DOMContentLoaded', () => {
    // --- 1. SELEÇÃO DE ELEMENTOS ---
    const elements = {
        menuToggleButton: document.getElementById('menuToggleButton'),
        closeMenuButton: document.getElementById('closeMenuButton'),
        sideMenu: document.getElementById('sideMenu'),
        menuOverlay: document.getElementById('menuOverlay'),
        mainContent: document.getElementById('mainContent'),
        tabs: document.querySelectorAll('.tab-button'),
        tabContents: document.querySelectorAll('#tabContentSection > .tab-content'),
        subTabsInstrucao: document.querySelectorAll('#tabInstrucaoTrabalho .subtab-button'),
        subTabContentsInstrucao: document.querySelectorAll('#subtabContentSectionInstrucao > .subtab-content'),
        pageTitle: document.getElementById('pageTitle'),
        detailPageMessageArea: document.getElementById('detailPageMessageArea'),
        userInfoContainer: document.getElementById('userInfoContainer'),
        // Modais
        stopReasonModal: document.getElementById('stopReasonModalDetails'),
        finalizeTaskModal: document.getElementById('finalizeTaskModalDetails'),
        ncModal: document.getElementById('ncModalDetails'),
        imageModal: document.getElementById('imageModal'),
        // Botões de Ação Principais
        resumeOrderActivityBtn: document.getElementById('resumeOrderActivityBtn'),
        stopOrderActivityBtn: document.getElementById('stopOrderActivityBtn'),
        finalizeOrderActivityBtn: document.getElementById('finalizeOrderActivityBtn'),
        ncOrderActivityBtn: document.getElementById('ncOrderActivityBtn'),
        // Containers de Conteúdo
        orderInfoSection: document.getElementById('orderInfoSection'),
        infoOrderStep: document.getElementById('infoOrderStep'),
        infoProduct: document.getElementById('infoProduct'),
        qtyPlanned: document.getElementById('qtyPlanned'),
        qtyProduced: document.getElementById('qtyProduced'),
        qtyRemaining: document.getElementById('qtyRemaining'),
        workforceLogsContainer: document.getElementById('workforceLogsContainer'),
        equipmentLogsContainer: document.getElementById('equipmentLogsContainer'),
        finishedActivityLogsContainer: document.getElementById('finishedActivityLogsContainer'),
        imageGallery: document.getElementById('imageGallery'),
        technicalDrawingViewer: document.getElementById('technicalDrawingViewer'),
        stlViewerContainer: document.getElementById('stlViewerContainer'),
        pdfListContainer: document.getElementById('pdfListContainer'),
        instrucaoPreparacao: document.getElementById('subtabPreparacao'),
        instrucaoExecucao: document.getElementById('subtabExecucao'),
        instrucaoConferencia: document.getElementById('subtabConferencia'),
    };

    let durationInterval = null;
    const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

    // --- 2. FUNÇÕES AUXILIARES E DE UI ---

    const ui = {
        openMenu: () => {
            elements.sideMenu?.classList.remove('-translate-x-full');
            elements.menuOverlay?.classList.remove('hidden');
        },
        closeMenu: () => {
            elements.sideMenu?.classList.add('-translate-x-full');
            elements.menuOverlay?.classList.add('hidden');
        },
        openModal: (modal) => modal?.classList.add('flex') || modal?.classList.remove('hidden'),
        closeModal: (modal) => modal?.classList.remove('flex') || modal?.classList.add('hidden'),
        showMessage: (text, type = 'info', area = elements.detailPageMessageArea) => {
            if (!area) return;
            area.textContent = text;
            area.className = 'p-3 my-2 rounded-md text-center text-sm min-h-[2.75rem] transition-opacity duration-300';
            const typeClasses = {
                success: 'bg-green-700 border border-green-500 text-green-100',
                error: 'bg-red-800 border border-red-600 text-red-200',
                info: 'bg-sky-700 border border-sky-500 text-sky-100'
            };
            area.classList.add(...(typeClasses[type] || typeClasses.info).split(' '));
            area.style.opacity = text ? '1' : '0';
            if (text && type !== 'error') {
                setTimeout(() => { area.style.opacity = '0'; }, 5000);
            }
        },
        updateTopActionButtonsState: (status) => {
            if (elements.resumeOrderActivityBtn) elements.resumeOrderActivityBtn.disabled = status !== 'Parado';
            if (elements.stopOrderActivityBtn) elements.stopOrderActivityBtn.disabled = status !== 'Em Andamento';
            if (elements.finalizeOrderActivityBtn) elements.finalizeOrderActivityBtn.disabled = status === 'Finalizado';
        },
        formatDate: (dateString) => dateString ? new Date(dateString).toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' }) : '-',
        formatDuration: (totalSeconds) => {
            if (totalSeconds === null || isNaN(totalSeconds) || totalSeconds < 0) return '-';
            const hours = Math.floor(totalSeconds / 3600);
            const minutes = Math.floor((totalSeconds % 3600) / 60);
            const seconds = Math.floor(totalSeconds % 60);
            return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        },
        updateRunningDurations: () => {
            document.querySelectorAll('.running-timer').forEach(timer => {
                const startTime = new Date(timer.dataset.startTime).getTime();
                if (isNaN(startTime)) return;
                timer.textContent = ui.formatDuration((Date.now() - startTime) / 1000);
            });
        },
        startDurationTimer: () => {
            if (durationInterval) clearInterval(durationInterval);
            ui.updateRunningDurations();
            durationInterval = setInterval(ui.updateRunningDurations, 1000);
        }
    };

    // --- 3. LÓGICA DE API ---

    const api = {
        getCookie: (name) => {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        },
        fetchJSON: async (url, options = {}) => {
            options.headers = {
                'Content-Type': 'application/json',
                'X-CSRFToken': api.getCookie('csrftoken'),
                ...options.headers,
            };
            const response = await fetch(url, options);
            if (!response.ok) {
                const errData = await response.json().catch(() => ({ error: `Erro HTTP ${response.status}` }));
                throw new Error(errData.error || errData.detail || `Erro HTTP ${response.status}`);
            }
            return response.status !== 204 ? response.json() : null;
        }
    };

    // --- 4. RENDERIZAÇÃO DE CONTEÚDO ---

    const render = {
        logsTable: (logs, container, headers, rowRenderer) => {
            if (!container) return;
            if (!logs || logs.length === 0) {
                container.innerHTML = `<p class="text-industrial-secondary p-2">Nenhum apontamento encontrado.</p>`;
                return;
            }
            const table = document.createElement('table');
            table.className = 'min-w-full divide-y divide-industrial-light text-sm';
            const thead = table.createTHead();
            thead.className = 'bg-industrial-light';
            const headerRow = thead.insertRow();
            headers.forEach(headerText => {
                const th = document.createElement('th');
                th.className = 'px-4 py-2 text-left font-medium text-industrial-secondary uppercase tracking-wider';
                th.textContent = headerText;
                headerRow.appendChild(th);
            });
            const tbody = table.createTBody();
            tbody.className = 'bg-industrial-medium divide-y divide-industrial-light';
            logs.forEach(log => rowRenderer(log, tbody));
            container.innerHTML = '';
            container.appendChild(table);
        },
        workforceLogRow: (log, tbody) => {
            const row = tbody.insertRow();
            const isOngoing = !log.end_date;
            const uniqueLogId = log.id || log.code;
            let durationHtml = isOngoing
                ? `<span class="running-timer font-mono" data-start-time="${log.start_date}">-</span>`
                : ui.formatDuration((new Date(log.end_date) - new Date(log.start_date)) / 1000);

            row.innerHTML = `
                <td class="px-4 py-2 whitespace-nowrap text-industrial-primary">${log.workforce_name || 'N/D'}</td>
                <td class="px-4 py-2 whitespace-nowrap text-industrial-primary">${ui.formatDate(log.start_date)}</td>
                <td class="px-4 py-2 whitespace-nowrap text-industrial-primary">${ui.formatDate(log.end_date)}</td>
                <td class="px-4 py-2 whitespace-nowrap text-industrial-primary text-right font-mono">${durationHtml}</td>
                <td class="px-4 py-2 whitespace-nowrap text-center space-x-2">
                    <button data-action="stop-log" data-log-id="${uniqueLogId}" data-log-type="workforce" class="text-yellow-400 hover:text-yellow-300 p-1" title="Parar Operador"><i class="fas fa-pause-circle fa-lg"></i></button>
                    <button data-action="finalize-log" data-log-id="${uniqueLogId}" data-log-type="workforce" class="text-green-400 hover:text-green-300 p-1" title="Finalizar Operador"><i class="fas fa-check-circle fa-lg"></i></button>
                    <button data-action="resume-log" data-log-id="${uniqueLogId}" data-log-type="workforce" class="text-blue-400 hover:text-blue-300 p-1" title="Retomar Operador"><i class="fas fa-play-circle fa-lg"></i></button>
                </td>
            `;
        },
        equipmentLogRow: (log, tbody) => {
            const row = tbody.insertRow();
            const isOngoing = !log.end_date;
            const uniqueLogId = log.id || log.code;
            let durationHtml = isOngoing
                ? `<span class="running-timer font-mono" data-start-time="${log.start_date}">-</span>`
                : ui.formatDuration((new Date(log.end_date) - new Date(log.start_date)) / 1000);

            row.innerHTML = `
                <td class="px-4 py-2 whitespace-nowrap text-industrial-primary">${log.equipment_description || 'N/D'}</td>
                <td class="px-4 py-2 whitespace-nowrap text-industrial-primary">${ui.formatDate(log.start_date)}</td>
                <td class="px-4 py-2 whitespace-nowrap text-industrial-primary">${ui.formatDate(log.end_date)}</td>
                <td class="px-4 py-2 whitespace-nowrap text-industrial-primary text-right font-mono">${durationHtml}</td>
                <td class="px-4 py-2 whitespace-nowrap text-center space-x-2">
                    <button data-action="stop-log" data-log-id="${uniqueLogId}" data-log-type="equipment" class="text-yellow-400 hover:text-yellow-300 p-1" title="Parar Equipamento"><i class="fas fa-pause-circle fa-lg"></i></button>
                    <button data-action="finalize-log" data-log-id="${uniqueLogId}" data-log-type="equipment" class="text-green-400 hover:text-green-300 p-1" title="Finalizar Equipamento"><i class="fas fa-check-circle fa-lg"></i></button>
                    <button data-action="resume-log" data-log-id="${uniqueLogId}" data-log-type="equipment" class="text-blue-400 hover:text-blue-300 p-1" title="Retomar Equipamento"><i class="fas fa-play-circle fa-lg"></i></button>
                </td>
            `;
        },
        finishedActivityLogsRow: (log, tbody) => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td class="px-4 py-2 whitespace-nowrap text-industrial-primary">${log.operator_name || 'N/D'}</td>
                <td class="px-4 py-2 whitespace-nowrap text-industrial-primary">${log.equipment_name || 'N/D'}</td>
                <td class="px-4 py-2 whitespace-nowrap text-industrial-primary">${ui.formatDate(log.start_date)}</td>
                <td class="px-4 py-2 whitespace-nowrap text-industrial-primary">${ui.formatDate(log.end_date)}</td>
                <td class="px-4 py-2 whitespace-nowrap text-industrial-primary text-right">${log.quantity_produced != null ? parseFloat(log.quantity_produced).toLocaleString('pt-BR') : '-'}</td>
            `;
        },
        media: (files, container, itemRenderer, emptyMessage) => {
            if (!container) return;
            container.innerHTML = '';
            if (!files || files.length === 0) {
                container.innerHTML = `<p class="text-industrial-secondary col-span-full p-2">${emptyMessage}</p>`;
                return;
            }
            files.forEach(file => container.innerHTML += itemRenderer(file));
        },
        imageItem: (file) => `
            <div class="gallery-item">
                <img src="${file.file_url}" alt="${file.description || 'Imagem'}" onclick="openImageModal('${file.file_url}')">
            </div>`,
        drawingItem: (file) => `
            <a href="${file.file_url}" target="_blank" class="flex items-center p-2 rounded-md hover:bg-industrial-light transition-colors">
                <i class="fas fa-drafting-compass mr-3 text-industrial-accent"></i>
                <span>${file.description || new URL(file.file_url).pathname.split('/').pop()}</span>
            </a>`,
        pdfItem: (file) => `
            <a href="${file.file_url}" target="_blank" class="flex items-center p-2 rounded-md hover:bg-industrial-light transition-colors">
                <i class="fas fa-file-pdf mr-3 text-industrial-accent"></i>
                <span>${file.description || new URL(file.file_url).pathname.split('/').pop()}</span>
            </a>`,
        stlItem: (file) => `
            <a href="${file.file_url}" download class="flex items-center p-2 rounded-md hover:bg-industrial-light transition-colors">
                <i class="fas fa-cube mr-3 text-industrial-accent"></i>
                <span>${file.description || new URL(file.file_url).pathname.split('/').pop()} (Download)</span>
            </a>`,
    };

    // --- 5. LÓGICA DE AÇÕES E EVENTOS ---

    const actions = {
        loadReasonsToSelect: async (reasonType, selectElement, messageArea) => {
            if (!selectElement || !messageArea) return;
            ui.showMessage('Carregando motivos...', 'info', messageArea);
            selectElement.innerHTML = '<option value="">Carregando...</option>';
            const endpoint = reasonType === 'stop' ? 'stop-reason' : 'non-conformance';
            try {
                const reasons = await api.fetchJSON(`${API_BASE_URL}/${endpoint}/?is_active=1`);
                const reasonList = Array.isArray(reasons) ? reasons : reasons.results || [];
                selectElement.innerHTML = '<option value="">Selecione um motivo...</option>';
                reasonList.forEach(reason => {
                    selectElement.innerHTML += `<option value="${reason.code}">${reason.description}</option>`;
                });
                ui.showMessage('', 'info', messageArea);
            } catch (error) {
                ui.showMessage(`Falha ao carregar motivos: ${error.message}`, 'error', messageArea);
            }
        },
        handleIndividualLogAction: async (logId, logType, action) => {
            const endpointType = logType === 'workforce' ? 'activity-workforce-log' : 'activity-equipment-log';
            const url = `${API_BASE_URL}/${endpointType}/${logId}/${action}/`;
            const method = (action === 'resume' || action === 'finalize') ? 'PATCH' : 'POST';
            try {
                const result = await api.fetchJSON(url, { method });
                ui.showMessage(result.message || `Ação ${action} executada com sucesso!`, 'success');
                page.init(); // Recarrega todos os dados da página
            } catch (error) {
                ui.showMessage(`Erro ao executar ação: ${error.message}`, 'error');
            }
        },
        submitStopReason: async () => {
            const logId = document.getElementById('stopModalLogIdDetails').value;
            const logType = document.getElementById('stopModalLogTypeDetails').value;
            const reasonId = document.getElementById('stopReasonSelectDetails').value;
            const modalMsgArea = document.getElementById('stopReasonModalMessageAreaDetails');

            if (!reasonId) return ui.showMessage('Selecione um motivo.', 'error', modalMsgArea);
            ui.showMessage('Registrando parada...', 'info', modalMsgArea);

            const endpointType = logType === 'activity' ? 'order-activity-progress' : (logType === 'workforce' ? 'activity-workforce-log' : 'activity-equipment-log');
            const url = `${API_BASE_URL}/${endpointType}/${logId}/stop/`;

            try {
                const result = await api.fetchJSON(url, {
                    method: 'POST',
                    body: JSON.stringify({ stop_reason_code: reasonId })
                });
                ui.showMessage(result.message || 'Parada registrada!', 'success');
                ui.closeModal(elements.stopReasonModal);
                page.init();
            } catch (error) {
                ui.showMessage(`Erro: ${error.message}`, 'error', modalMsgArea);
            }
        },
        submitFinalize: async () => {
            const activityProgressId = new URLSearchParams(window.location.search).get('activityId');
            const quantity = document.getElementById('finalizeQuantityInputDetails').value;
            const modalMsgArea = document.getElementById('finalizeTaskModalMessageAreaDetails');

            if (!quantity || parseFloat(quantity) < 0) {
                return ui.showMessage('Insira uma quantidade produzida válida.', 'error', modalMsgArea);
            }
            ui.showMessage('Finalizando atividade...', 'info', modalMsgArea);
            const url = `${API_BASE_URL}/order-activity-progress/${activityProgressId}/`;
            try {
                const result = await api.fetchJSON(url, {
                    method: 'PATCH',
                    body: JSON.stringify({ quantity: parseFloat(quantity), status: 'Finalizado' })
                });
                ui.showMessage(result.message || 'Atividade principal finalizada!', 'success');
                ui.closeModal(elements.finalizeTaskModal);
                page.init();
            } catch (error) {
                ui.showMessage(`Erro: ${error.message}`, 'error', modalMsgArea);
            }
        },
        submitNC: async () => {
            const activityProgressId = new URLSearchParams(window.location.search).get('activityId');
            const reasonId = document.getElementById('ncReasonSelectDetails').value;
            const quantity = document.getElementById('ncQuantityInputDetails').value;
            const modalMsgArea = document.getElementById('ncModalMessageAreaDetails');

            if (!reasonId) return ui.showMessage('Selecione um motivo de NC.', 'error', modalMsgArea);
            if (!quantity || parseFloat(quantity) <= 0) return ui.showMessage('Insira uma quantidade NC válida.', 'error', modalMsgArea);

            ui.showMessage('Registrando Não Conformidade...', 'info', modalMsgArea);
            const url = `${API_BASE_URL}/activity-non-conformance-log/`;
            try {
                await api.fetchJSON(url, {
                    method: 'POST',
                    body: JSON.stringify({
                        order_activity: activityProgressId,
                        non_conformance: reasonId,
                        quantity: parseFloat(quantity)
                    })
                });
                ui.showMessage('Não Conformidade registrada!', 'success');
                ui.closeModal(elements.ncModal);
            } catch (error) {
                ui.showMessage(`Erro: ${error.message}`, 'error', modalMsgArea);
            }
        },
    };

    // --- 6. INICIALIZAÇÃO DA PÁGINA ---

    const page = {
        init: async () => {
            const urlParams = new URLSearchParams(window.location.search);
            const activityProgressId = urlParams.get('activityId');

            if (!activityProgressId) {
                ui.showMessage('ID da atividade não fornecido na URL.', 'error');
                elements.orderInfoSection.innerHTML = '<p class="text-red-400 text-center">Erro: ID da atividade não encontrado.</p>';
                return;
            }

            try {
                const progressData = await api.fetchJSON(`${API_BASE_URL}/order-activity-progress/${activityProgressId}/`);

                // Renderiza as informações principais
                if (elements.infoOrderStep) elements.infoOrderStep.textContent = `OP: ${progressData.order_code} / Seq: ${progressData.sequence} - ${progressData.activity?.description || 'N/D'}`;
                if (elements.infoProduct) elements.infoProduct.textContent = `Cód: ${progressData.activity?.product_code || 'N/D'} - ${progressData.activity?.product_description || 'Produto não informado'}`;
                const planned = parseFloat(progressData.activity?.quantity_planned || 0);
                const produced = parseFloat(progressData.quantity || 0);
                if (elements.qtyPlanned) elements.qtyPlanned.textContent = planned.toLocaleString('pt-BR');
                if (elements.qtyProduced) elements.qtyProduced.textContent = produced.toLocaleString('pt-BR');
                if (elements.qtyRemaining) elements.qtyRemaining.textContent = (planned - produced).toLocaleString('pt-BR');
                ui.updateTopActionButtonsState(progressData.status);

                // Renderiza as mídias e instruções
                const productFiles = progressData.product_files || [];
                render.media(productFiles.filter(f => f.file_type === 'image'), elements.imageGallery, render.imageItem, 'Nenhuma imagem disponível.');
                render.media(productFiles.filter(f => f.file_type === 'drawing'), elements.technicalDrawingViewer, render.drawingItem, 'Nenhum desenho técnico disponível.');
                render.media(productFiles.filter(f => f.file_type === 'pdf'), elements.pdfListContainer, render.pdfItem, 'Nenhum documento PDF disponível.');
                render.media(productFiles.filter(f => f.file_type === 'stl'), elements.stlViewerContainer, render.stlItem, 'Nenhum arquivo STL disponível.');

                const instructions = progressData.work_instructions;
                if (elements.instrucaoPreparacao) elements.instrucaoPreparacao.innerHTML = instructions?.work_instruction_preparation || '<p>Não disponível.</p>';
                if (elements.instrucaoExecucao) elements.instrucaoExecucao.innerHTML = instructions?.work_instruction_execution || '<p>Não disponível.</p>';
                if (elements.instrucaoConferencia) elements.instrucaoConferencia.innerHTML = instructions?.work_instruction_conference || '<p>Não disponível.</p>';

                // Carrega e renderiza as tabelas de logs
                const [workforceLogs, equipmentLogs, finishedLogs] = await Promise.all([
                    api.fetchJSON(`${API_BASE_URL}/activity-workforce-log/?order_activity=${activityProgressId}`),
                    api.fetchJSON(`${API_BASE_URL}/activity-equipment-log/?order_activity=${activityProgressId}`),
                    api.fetchJSON(`${API_BASE_URL}/order-activity-progress/?order_code=${progressData.order_code}&activity__code=${progressData.activity?.code}&status=Finalizado`)
                ]);

                render.logsTable(workforceLogs.results || workforceLogs, elements.workforceLogsContainer, ['Operador', 'Início', 'Fim', 'Duração', 'Ações'], render.workforceLogRow);
                render.logsTable(equipmentLogs.results || equipmentLogs, elements.equipmentLogsContainer, ['Equipamento', 'Início', 'Fim', 'Duração', 'Ações'], render.equipmentLogRow);
                render.logsTable(finishedLogs.results || finishedLogs, elements.finishedActivityLogsContainer, ['Operador', 'Equipamento', 'Início', 'Fim', 'Qtd. Produzida'], render.finishedActivityLogsRow);

                ui.startDurationTimer();

            } catch (error) {
                ui.showMessage(`Falha ao carregar dados da página: ${error.message}`, 'error');
            }
        },
        setupEventListeners: () => {
            const activityProgressId = new URLSearchParams(window.location.search).get('activityId');

            // Menu
            elements.menuToggleButton?.addEventListener('click', ui.openMenu);
            elements.closeMenuButton?.addEventListener('click', ui.closeMenu);
            elements.menuOverlay?.addEventListener('click', ui.closeMenu);

            // Abas
            elements.tabs.forEach(tab => {
                tab.addEventListener('click', () => {
                    elements.tabs.forEach(t => t.classList.remove('active'));
                    tab.classList.add('active');
                    elements.tabContents.forEach(content => {
                        content.classList.toggle('active', content.id === tab.dataset.target);
                    });
                });
            });
            elements.subTabsInstrucao.forEach(subTab => {
                subTab.addEventListener('click', () => {
                    elements.subTabsInstrucao.forEach(st => st.classList.remove('active-subtab'));
                    subTab.classList.add('active-subtab');
                    elements.subTabContentsInstrucao.forEach(content => {
                        content.classList.toggle('active-subtab-content', content.id === subTab.dataset.subtarget);
                    });
                });
            });

            // Ações nos logs individuais
            document.getElementById('tabApontamentos')?.addEventListener('click', (event) => {
                const button = event.target.closest('button[data-action]');
                if (!button) return;
                const { action, logId, logType } = button.dataset;

                if (action === 'stop-log') {
                    document.getElementById('stopModalLogIdDetails').value = logId;
                    document.getElementById('stopModalLogTypeDetails').value = logType;
                    actions.loadReasonsToSelect('stop', document.getElementById('stopReasonSelectDetails'), document.getElementById('stopReasonModalMessageAreaDetails'));
                    ui.openModal(elements.stopReasonModal);
                } else if (action === 'resume-log' || action === 'finalize-log') {
                    actions.handleIndividualLogAction(logId, logType, action.replace('-log', ''));
                }
            });

            // Botões de Ação Principais
            elements.resumeOrderActivityBtn?.addEventListener('click', () => actions.handleIndividualLogAction(activityProgressId, 'activity', 'resume'));
            elements.stopOrderActivityBtn?.addEventListener('click', () => {
                document.getElementById('stopModalLogIdDetails').value = activityProgressId;
                document.getElementById('stopModalLogTypeDetails').value = 'activity';
                actions.loadReasonsToSelect('stop', document.getElementById('stopReasonSelectDetails'), document.getElementById('stopReasonModalMessageAreaDetails'));
                ui.openModal(elements.stopReasonModal);
            });
            elements.finalizeOrderActivityBtn?.addEventListener('click', () => ui.openModal(elements.finalizeTaskModal));
            elements.ncOrderActivityBtn?.addEventListener('click', () => {
                actions.loadReasonsToSelect('nc', document.getElementById('ncReasonSelectDetails'), document.getElementById('ncModalMessageAreaDetails'));
                ui.openModal(elements.ncModal);
            });

            // Botões dos Modais
            document.getElementById('submitStopReasonDetails')?.addEventListener('click', actions.submitStopReason);
            document.getElementById('submitFinalizeTaskDetails')?.addEventListener('click', actions.submitFinalize);
            document.getElementById('submitNcDetails')?.addEventListener('click', actions.submitNC);
            document.querySelector('[data-action="close-stop-modal-details"]')?.addEventListener('click', () => ui.closeModal(elements.stopReasonModal));
            document.querySelector('[data-action="close-finalize-modal-details"]')?.addEventListener('click', () => ui.closeModal(elements.finalizeTaskModal));
            document.querySelector('[data-action="close-nc-modal-details"]')?.addEventListener('click', () => ui.closeModal(elements.ncModal));
            document.getElementById('closeImageModal')?.addEventListener('click', () => ui.closeModal(elements.imageModal));
        }
    };

    page.setupEventListeners();
    page.init();
});