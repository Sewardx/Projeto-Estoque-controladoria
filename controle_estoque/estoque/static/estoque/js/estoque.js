$(document).ready(function () {
    const apiEndpoint = '/estoque/api/materiais/';
    const selectedItems = []; // Lista de itens selecionados
    const successModal = $('#successModal');
    const closeModalBtn = $('#closeModal, #okButton');

    // Inicializar Select2 e carregar materiais da API
    const initSelect2 = () => {
        $('#material-select').select2({
            placeholder: 'Selecione um material',
            minimumInputLength: 0,
            ajax: {
                url: apiEndpoint,
                dataType: 'json',
                delay: 250,
                processResults: (data) => {
                    return {
                        results: data.map(material => ({
                            id: material.id,
                            text: `${material.nome} (${material.tipo_produto} - Disponível: ${material.quantidade})`,
                            tipo_produto: material.tipo_produto,
                            quantidade_disponivel: material.quantidade,
                        })),
                    };
                },
                cache: true,
            },
            templateResult: function (data) {
                if (!data.id) return data.text;
                return $(`<span>${data.text}</span>`);
            },
            language: {
                searching: () => "Buscando materiais...",
                noResults: () => "Nenhum material encontrado",
            },
        });
    };

    // Atualizar tabela de materiais adicionados
    const atualizarTabela = () => {
        const tabelaBody = $('#materials-table-body');
        tabelaBody.empty();

        selectedItems.forEach(item => {
            tabelaBody.append(`
                <tr>
                    <td>${item.nome}</td>
                    <td>${item.tipo_produto}</td>
                    <td>${item.quantidade}</td>
                    <td>
                        <button type="button" class="btn btn-danger btn-sm remove-item" data-id="${item.id}">
                            Remover
                        </button>
                    </td>
                </tr>
            `);
        });
    };

    // Atualizar campos ocultos antes do envio
    const atualizarCamposOcultos = () => {
        const materials = [];
        const quantidades = [];

        selectedItems.forEach(item => {
            materials.push(item.id);
            quantidades.push(item.quantidade);
        });

        $('#materials').val(JSON.stringify(materials));
        $('#quantidades').val(JSON.stringify(quantidades));
    };

    // Adicionar item à lista
    $('#add-material').on('click', function () {
        const materialSelect = $('#material-select');
        const quantidadeInput = $('#quantidade');

        const materialId = parseInt(materialSelect.val());
        const materialNome = materialSelect.find('option:selected').text();
        const quantidade = parseInt(quantidadeInput.val());
        const tipoProduto = materialSelect.select2('data')[0]?.tipo_produto;
        const quantidadeDisponivel = materialSelect.select2('data')[0]?.quantidade_disponivel;

        if (!materialId || !quantidade || quantidade <= 0) {
            alert('Selecione um material válido e insira uma quantidade maior que 0.');
            return;
        }

        if (quantidade > quantidadeDisponivel) {
            alert(`Quantidade indisponível. Disponível: ${quantidadeDisponivel}`);
            return;
        }

        if (selectedItems.some(item => item.id === materialId)) {
            alert('Este material já foi adicionado.');
            return;
        }

        selectedItems.push({
            id: materialId,
            nome: materialNome,
            quantidade: quantidade,
            tipo_produto: tipoProduto,
        });

        atualizarTabela();
        atualizarCamposOcultos();

        materialSelect.val(null).trigger('change');
        quantidadeInput.val('');
    });

    // Remover item da lista
    $('#materials-table-body').on('click', '.remove-item', function () {
        const materialId = parseInt($(this).data('id'));
        const index = selectedItems.findIndex(item => item.id === materialId);

        if (index !== -1) {
            selectedItems.splice(index, 1);
        }

        atualizarTabela();
        atualizarCamposOcultos();
    });

    // Validação no envio do formulário com modal de sucesso
    $('#requisicao-form').on('submit', function (e) {
        if (selectedItems.length === 0) {
            e.preventDefault();
            alert('Adicione pelo menos um material antes de enviar a requisição.');
            return false;
        }

        atualizarCamposOcultos();

        // Prevent default form submission for demonstration
        e.preventDefault();

        // Simulate AJAX form submission
        $.ajax({
            url: $(this).attr('action'),
            method: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                // Show success modal
                successModal.addClass('show');

                // Clear selected items and table
                selectedItems.length = 0;
                atualizarTabela();
                atualizarCamposOcultos();
            },
            error: function(xhr) {
                alert('Erro ao enviar requisição. Tente novamente.');
            }
        });
    });

    // Modal close handlers
    closeModalBtn.on('click', function() {
        successModal.removeClass('show');
    });

    // Close modal when clicking outside
    successModal.on('click', function(e) {
        if (e.target === this) {
            $(this).removeClass('show');
        }
    });

    // Inicializar o Select2
    initSelect2();
});