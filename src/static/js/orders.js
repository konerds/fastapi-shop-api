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
    elParagraphTotalPrice.innerText = `총 주문 가격: ${price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}원`;
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
    document.getElementById("total-price").innerText = `총 주문 가격: ${(price * quantity).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}원`;
}

function createOrder() {
    var productId = document.getElementById("options-product").value;
    var quantity = document.getElementById("quantity").value;
    var address = document.getElementById("address").value;
    if (!productId) {
        alert("주문하실 상품을 선택해주세요...");
        return;
    }
    if (!quantity) {
        alert("주문 수량을 입력해주세요...");
        return;
    }
    if (!address) {
        alert("배송 주소를 입력해주세요...");
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
                quantity: quantity,
                address: address
            }
        )
    })
        .then(response => response.json().then(dataRaw => {
            if (!response.ok) {
                throw new Error(dataRaw.detail || "주문 접수에 실패하였습니다...");
            }
            location.reload();
        }))
        .catch((error) => {
            alert(error.message);
            console.error('Error:', error);
        });
}

function cancelOrder(orderId) {
    if (!confirm('주문을 취소하시겠습니까?')) {
        return;
    }
    fetch('/api/orders/' + orderId, {
        method: 'DELETE',
    })
        .then(response => {
            if (response.status === 204) {
                return location.reload();
            }
            return response.json().then(dataRaw => {
                throw new Error(dataRaw.detail || "주문 취소에 실패하였습니다...");
            });
        })
        .catch((error) => {
            alert(error.message);
            console.error('Error:', error);
        })
        .finally(() => location.reload());
}