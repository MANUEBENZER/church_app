<script>
function togglePromiseFields() {
    const type = document.getElementById("promiseType").value;
    document.getElementById("moneyField").style.display = type === "money" ? "block" : "none";
    document.getElementById("itemField").style.display = type === "item" ? "block" : "none";
}
</script>
