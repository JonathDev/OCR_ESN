document.addEventListener('DOMContentLoaded', function() {
    attachEventListeners();
});

function attachEventListeners() {
    document.querySelectorAll('.flip-card-btn-turn-to-back').forEach(button => {
        button.addEventListener('click', function() {
            showVerso(this);
        });
    });

    document.querySelectorAll('.flip-card-btn-turn-to-front').forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.flip-card');
            card.classList.remove('do-flip');
        });
    });

    document.querySelectorAll('.btn-supprimer').forEach(button => {
        button.addEventListener('click', function() {
            removeProductLine(this);
        });
    });

    document.querySelectorAll('.btn-ajouterProduit').forEach(button => {
        button.addEventListener('click', function() {
            const cardBody = this.closest('.card-body');
            const productUl = cardBody.querySelector('.product.list-group');
            addNewProductLine(productUl);
        });
    });

    document.querySelectorAll('.flip-card').forEach(cardElement => {
        cardElement.addEventListener('input', function(event) {
            if (event.target.classList.contains('quantite') || event.target.classList.contains('prix-unitaire')) {
                updateTotalForCard(this.closest('.flip-card'));
            }
        });
    });
}

function showVerso(element) {
    const card = element.closest('.flip-card');
    card.classList.add('do-flip');
    updateTotalForCard(card);
}


function showRecto(element) {
    const card = element.closest('.flip-card');
    // Supprimer la classe qui fait tourner la carte pour montrer le verso, pour revenir au recto
    card.classList.remove('do-flip');
}


document.querySelectorAll('.btn-ajouterProduit').forEach(button => {
    button.addEventListener('click', function() {
        const cardBody = this.closest('.card-body');
        console.log('CardBody:', cardBody); // Doit afficher l'élément cardBody, sinon null
        const productUl = cardBody ? cardBody.querySelector('.product.list-group') : null;
        console.log('ProductUl:', productUl); // Doit afficher l'élément UL, sinon null
        if (productUl) {
            addNewProductLine(productUl);
        } else {
            console.error('UL non trouvé pour ajouter un produit');
        }
    });
});

function addNewProductLine(ul) {
    const li = document.createElement('li');
    li.className = "list-group-item";
    li.innerHTML = `
        <div class="form-group">
            <input type="number" class="form-control quantite" value="1" placeholder="Quantité" min="1">
        </div>
        <div class="form-group">
            <input type="text" class="form-control prix-unitaire" value="" placeholder="Prix unitaire">
        </div>
        <button class="btn btn-danger btn-supprimer">Supprimer</button>`;
    ul.appendChild(li);

    // Mettre à jour les écouteurs pour le nouveau bouton supprimer
    li.querySelector('.btn-supprimer').addEventListener('click', function() {
        removeProductLine(this);
    });

    // Mettre à jour le total après ajout d'un produit
    updateTotalForCard(ul.closest('.flip-card'));
}

function removeProductLine(element) {
    const cardElement = element.closest('.flip-card');
    element.closest('li.list-group-item').remove();
    updateTotalForCard(cardElement);
}

function updateTotalForCard(cardElement) {
    let total = 0;
    const productItems = cardElement.querySelectorAll('.list-group-item:not(:last-child)');

    productItems.forEach(item => {
        console.log(item.querySelector('.quantite'), item.querySelector('.prix-unitaire'));
        const quantiteInput = item.querySelector('.quantite');
        const prixUnitaireInput = item.querySelector('.prix-unitaire');
        
        const quantite = quantiteInput ? Number(quantiteInput.value) : 0;
        const prixUnitaire = prixUnitaireInput ? Number(prixUnitaireInput.value) : 0;
        
        total += quantite * prixUnitaire;
    });

    const totalElement = cardElement.querySelector('.total');
    if (totalElement) {
        totalElement.textContent = total.toFixed(2) + ' €';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    attachEventListeners();
});

function attachEventListeners() {
    // Pour chaque bouton d'ajout de produit dans les cartes
    document.querySelectorAll('.btn-ajouterProduit').forEach(button => {
        button.addEventListener('click', function() {
            const cardBody = this.closest('.card-body');
            const productUl = cardBody.querySelector('.product.list-group');
            addNewProductLine(productUl);
        });
    });

    attachEventListenersToUpdateAndDeleteButtons();
    updateAllCardsTotals();
}

function addNewProductLine(ul) {
    const li = document.createElement('li');
    li.className = "list-group-item";
    li.innerHTML = `
        <div class="form-group">
            <input type="number" class="form-control quantite" placeholder="Quantité" min="1" value="1">
        </div>
        <div class="form-group">
            <input type="text" class="form-control prix-unitaire" placeholder="Prix unitaire">
        </div>
        <button class="btn btn-danger btn-supprimer" onclick="removeProductLine(this);">Supprimer</button>
    `;
    ul.appendChild(li);

    // Mettre à jour le total pour la carte
    updateTotalForCard(ul.closest('.flip-card'));
}

function removeProductLine(element) {
    const cardElement = element.closest('.flip-card');
    element.closest('li.list-group-item').remove();
    updateTotalForCard(cardElement);
}

function updateTotalForCard(cardElement) {
    let total = 0;
    const productItems = cardElement.querySelectorAll('.product.list-group .list-group-item:not(:last-child)');
    productItems.forEach(item => {
        const quantite = Number(item.querySelector('.quantite').value) || 0;
        const prixUnitaire = Number(item.querySelector('.prix-unitaire').value) || 0;
        total += quantite * prixUnitaire;
    });

    const totalElement = cardElement.querySelector('.total');
    if (totalElement) {
        totalElement.textContent = `${total.toFixed(2)} €`;
    }
}

function attachEventListenersToUpdateAndDeleteButtons() {
    document.querySelectorAll('.btn-supprimer').forEach(button => {
        button.addEventListener('click', function() {
            removeProductLine(this);
        });
    });

    // Ajoutez ici d'autres logiques pour les boutons update si nécessaire
}




// pas de modife ici ceci fonctionne bien 

async function updateInvoice(invoiceNumber) {
    console.log("Je rentre dans la fonction updateInvoice");
    console.log(`updateInvoice appelé pour la facture ${invoiceNumber}`);

    try {
        // Récupération des données modifiées
        const customerNameElement = document.getElementById(`customer_name_${invoiceNumber}`);
        console.log('customerNameElement:', customerNameElement);
        const customerName = customerNameElement.value;

        const adresseCustomerElement = document.getElementById(`adresse_customer_${invoiceNumber}`);
        console.log('adresseCustomerElement:', adresseCustomerElement);
        const adresseCustomer = adresseCustomerElement.value;

        const categoryElement = document.getElementById(`invoice.category_${invoiceNumber}`);
        console.log('categoryElement:', categoryElement);
        const category = categoryElement ? categoryElement.value : '';


        const total_priceElement = document.getElementById(`total_span_${invoiceNumber}`);
        console.log('total_priceElement:', total_priceElement);
        const total_price = parseFloat(total_priceElement.textContent);


        const paidElement = document.getElementById(`paid_${invoiceNumber}`);
        console.log('paidElement:', paidElement);
        const paid = paidElement.checked;

        // Collecte des données des produits
        const products = [];
        const productElements = document.querySelectorAll(`[data-invoice-number="${invoiceNumber}"] .product-info`);
        productElements.forEach(el => {
            const productID = el.dataset.productId;
            const name_productElement = document.getElementById(`product_name_${invoiceNumber}_${productID}`);
            console.log('name_productElement:', name_productElement);
            const name_product = name_productElement.value;

            const quantityElement = document.getElementById(`product_quantity_${invoiceNumber}_${productID}`);
            console.log('quantityElement:', quantityElement);
            const quantity = parseInt(quantityElement.value, 10);

            const unit_priceElement = document.getElementById(`product_unit_price_${invoiceNumber}_${productID}`);
            console.log('unit_priceElement:', unit_priceElement);
            const unit_price = parseFloat(unit_priceElement.value);

            products.push({ productID, name_product, quantity, unit_price });
        });

        const data = {
            customer_name: customerName, // Changez de customerName à customer_name
            adresse_customer: adresseCustomer, // Changez de adresseCustomer à adresse_customer
            category: category,
            total_price: total_price, // Assurez-vous que ce nom correspond
            paid: paid,
            products: products
        };

        console.log(`Données envoyées :`, data);

        const response = await fetch(`/search/${invoiceNumber}/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            console.log('Facture mise à jour avec succès.');
            // Ajouter une logique pour rafraîchir les données affichées ou informer l'utilisateur du succès
        } else {
            console.error('Erreur lors de la mise à jour de la facture.');
            // Traiter les erreurs retournées par le serveur si nécessaire
        }
    } catch (error) {
        console.error('Erreur :', error);
    }
}




function togglePaidStatus(checkbox, invoiceNumber) {
    console.log(`togglePaidStatus appelé pour la facture ${invoiceNumber}`);
    const isPaid = checkbox.checked;
    console.log(`Facture ${invoiceNumber} mise à jour comme ${isPaid ? 'payée' : 'non payée'}.`);

    // Mise à jour pour correspondre à la nouvelle structure d'ID
    const invoiceElement = document.getElementById(invoiceNumber); // Utilisez directement invoiceNumber
    if (invoiceElement) {
        if (isPaid) {
            invoiceElement.classList.remove('card-unpaid');
            invoiceElement.classList.add('card-paid');
            invoiceElement.style.boxShadow = "2px -2px 4px 3px rgba(0, 255, 0, 0.6)";
        } else {
            invoiceElement.classList.remove('card-paid');
            invoiceElement.classList.add('card-unpaid');
            invoiceElement.style.boxShadow = "2px -2px 4px 3px rgba(255, 0, 0, 0.6)";
        }
    } else {
        console.error('Element de facture introuvable.');
    }
}