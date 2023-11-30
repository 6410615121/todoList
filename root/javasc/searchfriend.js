document.addEventListener('DOMContentLoaded', function () {
    const friendItems = document.querySelectorAll('.friendrequest_container');
    const friendSearch = document.getElementById('friendSearch');

    friendSearch.addEventListener('input', function () {
        const searchQuery = this.value.toLowerCase();

        friendItems.forEach(function (friendItem) {
            const friendUsername = friendItem.querySelector('.friendrequest_content').innerText.toLowerCase();

            if (friendUsername.includes(searchQuery)) {
                friendItem.style.display = 'block';
            } else {
                friendItem.style.display = 'none';
            }
        });
    });
});