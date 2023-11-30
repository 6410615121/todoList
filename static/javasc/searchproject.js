document.addEventListener('DOMContentLoaded', function () {
    const projectItems = document.querySelectorAll('.project-item');


    document.getElementById('projectSearch').addEventListener('input', function () {
        const searchQuery = this.value.toLowerCase();

        projectItems.forEach(function (projectItems) {
            const projectname = projectItems.querySelector('.project_name').innerText.toLowerCase();
            

            if (projectname.includes(searchQuery)) {
                projectItems.style.display = 'block';
            } else {
                projectItems.style.display = 'none';
            }
        });
    });

    
});
