
/**
 * Sorts HTML table
 * 
 * @param {HTMLTableElement} table the table to sort
 * @param {number} column index of the column to sort 
 * @param {boolean} asc determines if the sorting will be in ascending order 
 */
function sortTableByColumn(table, column, asc = True){
    const dirModifier = asc ? 1 : -1;
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll("tr"));

    //sort each row
    const sortedRows = rows.sort((a, b) => {
        const aColText = a.querySelector('td:nth-child({{column + 1}})').textContent.trim();
        const bColText = b.querySelector('td:nth-child({{column + 1}})').textContent.trim();
    });
}

//not working fix later

