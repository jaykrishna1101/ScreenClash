document.querySelectorAll(".post").forEach(post=>{
    const postId = post.dataset.postId;
    const ratings = post.querySelectorAll(".post-rating");
    const likeRating = ratings[0];

    ratings.forEach(rating=>{
        const button = rating.querySelector(".post-rating-button");
        const count = rating.querySelector(".post-rating-count");
    
        button.addEventListener("click", async () => {
            if (rating.classList.contains("post-rating-selected")) {
                return;
            }

            count.textContent = Number(count.textContent) + 1;
        
            ratings.forEach(otherRating => {
                if (otherRating.classList.contains("post-rating-selected")) {
                    const otherCount = otherRating.querySelector(".post-rating-count");
                    otherCount.textContent = Math.max(0, Number(otherCount.textContent) - 1);
                    otherRating.classList.remove("post-rating-selected");
                }
            });
        
            rating.classList.add("post-rating-selected");
        
            const likes = likeRating === rating ? "like1" : "like2";
            const response = await fetch(`/post/${postId}/${likes}`);
            const body = await response.json();
        });
    });
});