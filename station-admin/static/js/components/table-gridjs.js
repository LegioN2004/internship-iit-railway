fetch("http://127.0.0.1:5000/trains")
  .then((res) => res.json())
  .then((data) => {
    // Transform your data to gridjs format: [[id, name, status], ...]
    const tableData = data.map((item) => [item.id, item.name, item.status]);
    new gridjs.Grid({
      columns: [
        { name: "Sl no.", width: "auto" },
        {
          name: "Train Name",
          width: "auto",
          formatter: (cell, row) => {
            const trainId = row.cells[0].data;
            const trainStatus = row.cells[2].data;
            return gridjs.html(
              `<a href="/train-report?name=${encodeURIComponent(
                cell
              )}&status=${trainStatus}&id=${trainId}" style="color: #011bff; text-decoration: none;">${cell}</a>`
            );
          },
        },
        {
          name: "Train Status",
          formatter: (cell, row) => {
            const trainName = row.cells[1].data;
            const trainId = row.cells[0].data;
            const isFinished = cell === "Finished";
            const bgColor = isFinished ? "#28a745" : "#dc3545";
            const hoverColor = isFinished ? "#218838" : "#c82333";

            return gridjs.html(
              `<a href="/train-report?name=${encodeURIComponent(
                trainName
              )}&status=${cell}&id=${trainId}"
                 style="background-color: ${bgColor};
                        color: white;
                        padding: 6px 12px;
                        border-radius: 4px;
                        text-decoration: none;
                        font-weight: 500;
                        display: inline-block;
                        transition: all 0.3s ease;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);"
                 onmouseover="this.style.backgroundColor='${hoverColor}';
                              this.style.transform='translateY(-1px)';
                              this.style.boxShadow='0 4px 8px rgba(0,0,0,0.2)';"
                 onmouseout="this.style.backgroundColor='${bgColor}';
                             this.style.transform='translateY(0px)';
                             this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)';">
                ${cell}
              </a>`
            );
          },
        },
      ],
      sort: true,
      resizable: true,
      pagination: true,
      fixedHeader: true,
      height: "auto",
      data: tableData,
    }).render(document.getElementById("table-fixed-header"));
  })
  .catch((error) => {
    console.log(error);
  });
