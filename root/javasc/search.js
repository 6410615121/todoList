function setupSearch(taskItems, searchElement, taskClass) {
    searchElement.addEventListener('input', function () {
        const searchQuery = this.value.toLowerCase();

        taskItems.forEach(function (taskItem) {
            const taskTitle = taskItem.querySelector(`.${taskClass}`).innerText.toLowerCase();
            const description = taskItem.querySelector('.description').innerText.toLowerCase();

            if (taskTitle.includes(searchQuery) || description.includes(searchQuery)) {
                taskItem.style.display = 'block';
            } else {
                taskItem.style.display = 'none';
            }
        });
    });
}
