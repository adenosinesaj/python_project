document.addEventListener("DOMContentLoaded", function () {
  const uploadInput = document.getElementById("profile-upload");
  const previewImg = document.getElementById("profile-preview");
  const saveBtn = document.getElementById("save-btn");
  const editableFields = document.querySelectorAll(".editable-field");

  /**
   * Detects if any form inputs or file uploads have changed
   * and toggles the state of the save button accordingly.
   */
  function detectChanges() {
    if (!saveBtn) return;

    let changesMade = false;

    // Check text/textarea inputs
    editableFields.forEach((field) => {
      if (field.value !== field.defaultValue) {
        changesMade = true;
      }
    });

    // Check image file input
    if (uploadInput && uploadInput.files && uploadInput.files.length > 0) {
      changesMade = true;
    }

    // Toggle button state
    if (changesMade) {
      saveBtn.disabled = false;
      saveBtn.classList.add("active");
    } else {
      saveBtn.disabled = true;
      saveBtn.classList.remove("active");
    }
  }

  /**
   * Previews the uploaded profile picture in real-time.
   */
  function previewImage(event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        if (previewImg) {
          previewImg.src = e.target.result;
        }
      };
      reader.readAsDataURL(file);
    }
    detectChanges();
  }

  // Attach event listeners to input fields
  editableFields.forEach((field) => {
    field.addEventListener("input", detectChanges);
  });

  if (uploadInput) {
    uploadInput.addEventListener("change", previewImage);
  }

  // Initial check on load
  detectChanges();
});