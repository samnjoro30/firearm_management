document.addEventListener('DOMContentLoaded', function() {
    fetchTransaction();
});
function fetchTransaction(){
    fetch('/api/transaction')
        .then(response => response.json())
        .then(data => {
            console.log('gun data', data);
            const transactionTable = document.getElementById('transaction-type').getElementsByTagName('tbody')[0];
            data.forEach(transaction => {
                let row = transactionTable.insertRow();
                row.insertCell(0).innerText = transaction.transactionId;
                row.insertCell(1).innerText = transaction.serialNumber;
                row.insertCell(2).innerText = transaction.Police_id;
                row.insertCell(3).innerText = transaction.transaction_type;
                row.insertCell(4).innerText = transaction.transaction_date;
            });
        })
        .catch(error => console.error('Error fetching transactions:', error));
}
