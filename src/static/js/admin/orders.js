function handlerOnChangeOptions(e) {
    var elSelectProducts = e.target;
    var selectedIdx = elSelectProducts.selectedIndex;
    var elInputQuantity = document.getElementById("quantity");
    var elParagraphTotalPrice = document.getElementById("total-price");
    if (!selectedIdx) {
        elInputQuantity.style.display = "none";
        elParagraphTotalPrice.innerText = '';
        return;
    }
    var pdt = elSelectProducts.options[selectedIdx];
    var price = pdt.getAttribute("data-price");
    if (+price < 0) {
        return;
    }
    var stock = pdt.getAttribute("data-stock");
    if (!stock) {
        return;
    }
    elInputQuantity.setAttribute("max", stock);
    elInputQuantity.setAttribute("value", 1)
    elInputQuantity.style.display = "block";
    elParagraphTotalPrice.innerText = `총 주문 가격: ${price}원`;
}

function handlerOnChangeQuantity(e) {
    var elSelectProducts = document.getElementById("options-product");
    var selectedIdx = elSelectProducts.selectedIndex;
    if (!selectedIdx) {
        return;
    }
    var price = elSelectProducts.options[selectedIdx].getAttribute("data-price");
    if (+price < 0) {
        return;
    }
    var quantity = +e.target.value;
    if (!quantity) {
        quantity = 1;
    } else {
        var max = +e.target.max;
        if (quantity > max) {
            quantity = max;
        }
    }
    document.getElementById("quantity").value = quantity;
    document.getElementById("total-price").innerText = `총 주문 가격: ${price * quantity}원`;
}

function createOrder() {
    var productId = document.getElementById("options-product").value;
    var quantity = document.getElementById('quantity').value;
    if (!productId || !quantity) {
        alert("주문하실 상품을 선택해주세요...");
        return;
    }
    if (!quantity) {
        alert("주문 수량을 입력해주세요...");
        return;
    }
    fetch('/api/orders', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(
            {
                product_id: productId,
                quantity: quantity
            }
        )
    })
        .then(response => response.json())
        .then(_ => {
            location.reload();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function deleteOrder(orderId) {
    if (!confirm('주문을 삭제하시겠습니까? (주문 이력 삭제는 권장되지 않습니다)')) {
        return;
    }
    fetch('/api/admin/orders/' + orderId, {
        method: 'DELETE',
    })
        .catch((error) => {
            console.error('Error:', error);
        }).finally(() => {
        location.reload();
    });
}