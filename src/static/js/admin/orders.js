function putOrderStatus(orderId, status) {
    if (!confirm(`주문 상태를 ${status === "proceeding" ? "주문 진행" : status === "completed" ? "결제 완료" : "취소"} 처리하시겠습니까?`)) {
        return;
    }
    fetch(`/api/admin/orders/${orderId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            status
        })
    })
        .then(response => response.json().then(dataRaw => {
            if (!response.ok) {
                throw new Error(dataRaw.detail || "주문 상태 변경에 실패하였습니다...");
            }
            location.reload();
        }))
        .catch((error) => {
            alert(error.message);
            console.error('Error:', error);
        });
}

function putOrderDeliveryStatus(orderId, status) {
    if (!confirm(`배송 상태를 ${status === "pending" ? "배송 대기" : status === "proceeding" ? "배송 진행" : status === "completed" ? "배송 완료" : "취소"} 처리하시겠습니까?`)) {
        return;
    }
    fetch(`/api/admin/orders/${orderId}/delivery`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            status
        })
    })
        .then(response => response.json().then(dataRaw => {
            if (!response.ok) {
                throw new Error(dataRaw.detail || "배송 상태 변경에 실패하였습니다...");
            }
            location.reload();
        }))
        .catch((error) => {
            alert(error.message);
            console.error('Error:', error);
        });
}

function deleteOrder(orderId) {
    if (!confirm('주문 이력을 삭제하시겠습니까? (권장되지 않습니다)')) {
        return;
    }
    fetch(`/api/admin/orders/${orderId}`, {
        method: 'DELETE',
    })
        .then(response => {
            if (response.status === 204) {
                return location.reload();
            }
            return response.json().then(dataRaw => {
                throw new Error(dataRaw.detail || "주문 이력 삭제에 실패하였습니다...");
            });
        })
        .catch((error) => {
            alert(error.message);
            console.error('Error:', error);
        });
}