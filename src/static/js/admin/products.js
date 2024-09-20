function createProduct() {
    var name = document.getElementById('new-product-name').value;
    if (!name) {
        alert("상품 이름을 입력해주세요...")
        return;
    }
    var price = document.getElementById('new-product-price').value;
    if (+price < 0) {
        alert("상품 가격을 올바르게 입력해주세요...")
        return;
    }
    var stock = document.getElementById('new-product-stock').value;
    if (+stock < 0) {
        alert("상품 재고를 올바르게 입력해주세요...")
        return;
    }
    fetch('/api/admin/products', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name,
            price,
            stock
        })
    })
        .then(response => response.json())
        .then(_ => location.reload())
        .catch((error) => console.error('Error:', error));
}

function putProduct(id, pdt) {
    fetch(`/api/admin/products/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(pdt)
    })
        .then(async (response) => {
            if (!response.ok) {
                throw new Error((await response.json()).detail || "상품 수정에 실패하였습니다...");
            }
            return response.json();
        })
        .catch((error) => {
            alert(error.message);
            console.error('Error:', error);
            location.reload();
        });
}


function toggleEdit(id, doNotUpdate = false) {
    if (doNotUpdate) {
        location.reload();
        return;
    }
    if (+id < 0) {
        alert("올바르지 않은 상품입니다...")
        return;
    }
    var elInputName = document.getElementById('name-' + id);
    var name = elInputName.value;
    if (!name) {
        alert("상품 이름을 입력해주세요...")
        return;
    }
    var elInputPrice = document.getElementById('price-' + id);
    var price = +elInputPrice.value;
    if (price < 0) {
        alert("상품 가격을 올바르게 입력해주세요...")
        return;
    }
    var elInputStock = document.getElementById('stock-' + id);
    var stock = +elInputStock.value;
    if (stock < 0) {
        alert("상품 재고를 올바르게 입력해주세요...")
        return;
    }
    var isReadOnly = elInputName.readOnly;
    var elSpanEditButtonText = document.getElementById("edit-button-text");
    if (!doNotUpdate && !isReadOnly) {
        putProduct(id, {
            name,
            price,
            stock
        });
    }
    elSpanEditButtonText.innerText = isReadOnly ? "완료" : "수정";
    elInputName.readOnly = elInputPrice.readOnly = elInputStock.readOnly = !isReadOnly;
    document.getElementsByClassName("btn-cancel")[0].style.display = isReadOnly ? "inline-block" : "none";
}