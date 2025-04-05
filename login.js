document.addEventListener("DOMContentLoaded", function () {
    function toggleForm(event) {
        event.preventDefault();

        const formTitle = document.getElementById("form-title");
        const authForm = document.getElementById("auth-form");
        const toggleText = document.getElementById("toggle-form");

        // Start fade-out transition
        authForm.classList.add("form-transition");
        authForm.classList.remove("show");

        setTimeout(() => {
            if (formTitle.innerText === "Login") {
                // Switch to Register form
                formTitle.innerText = "Register";
                authForm.innerHTML = `
                    <input type="text" placeholder="Full Name" required>
                    <input type="email" placeholder="Email" required>
                    <input type="password" placeholder="Password" required>
                    <button type="submit">Sign Up</button>
                `;
                toggleText.innerHTML = `Already have an account? <a href="#" id="toggle-btn">Login</a>`;
            } else {
                // Switch back to Login form
                formTitle.innerText = "Login";
                authForm.innerHTML = `
                    <input type="email" id="email" placeholder="Email" required>
                    <input type="password" id="password" placeholder="Password" required>
                    <div class="options">
                        <label>
                            <input type="checkbox"> Remember Me
                        </label>
                        <a href="#">Forget Password</a>
                    </div>
                    <button type="submit">Log in</button>
                `;
                toggleText.innerHTML = `Don't have an account? <a href="#" id="toggle-btn">Register</a>`;
            }

            // Add event listener again to new button
            document.getElementById("toggle-btn").addEventListener("click", toggleForm);

            // Start fade-in transition
            authForm.classList.add("show");
            authForm.classList.remove("form-transition");
        }, 500);
    }

    // Initial event listener
    document.getElementById("toggle-btn").addEventListener("click", toggleForm);
});
