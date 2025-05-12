/**
 * Utility functions for handling common language-specific text
 */

/**
 * Get text based on the current language
 * @param {string} currentLanguage - Current language code (en, es, ru)
 * @param {Object} options - Object containing text for each language 
 * @returns {string} - Localized text
 */
export const getLocalizedText = (currentLanguage, options) => {
  if (options[currentLanguage]) {
    return options[currentLanguage];
  }
  return options.en || "";  // Default to English
};

/**
 * Get patient information field labels based on language
 * @param {string} currentLanguage - Current language code
 * @returns {Object} - Object with localized field labels
 */
export const getPatientInfoLabels = (currentLanguage) => {
  switch(currentLanguage) {
    case 'es':
      return {
        patientName: "Nombre del Paciente",
        patientAge: "Edad del Paciente",
        relationship: "Su relación con el paciente"
      };
    case 'ru':
      return {
        patientName: "Имя Пациента",
        patientAge: "Возраст Пациента",
        relationship: "Ваше отношение к пациенту"
      };
    default:
      return {
        patientName: "Patient Name",
        patientAge: "Patient Age",
        relationship: "Your relationship to patient"
      };
  }
};

/**
 * Get form actions text based on language
 * @param {string} currentLanguage - Current language code
 * @returns {Object} - Object with localized action text
 */
export const getFormActionText = (currentLanguage) => {
  switch(currentLanguage) {
    case 'es':
      return {
        submit: "Enviar Evaluación",
        processing: "Procesando...",
        exportPDF: "Exportar como PDF",
        exporting: "Exportando..."
      };
    case 'ru':
      return {
        submit: "Отправить Оценку",
        processing: "Обработка...",
        exportPDF: "Экспорт в PDF",
        exporting: "Экспорт..."
      };
    default:
      return {
        submit: "Submit Assessment",
        processing: "Processing...",
        exportPDF: "Export as PDF",
        exporting: "Exporting..."
      };
  }
};

/**
 * Get error and success messages based on language
 * @param {string} currentLanguage - Current language code
 * @returns {Object} - Object with localized messages
 */
export const getLocalizedMessages = (currentLanguage) => {
  switch(currentLanguage) {
    case 'es':
      return {
        pdfSuccess: 'PDF generado con éxito. Revise la carpeta de exportaciones.',
        pdfError: 'Error al exportar PDF. Inténtelo de nuevo.',
        assessmentError: 'Error en la evaluación. Inténtelo de nuevo.'
      };
    case 'ru':
      return {
        pdfSuccess: 'PDF успешно создан. Проверьте папку экспорта.',
        pdfError: 'Ошибка при экспорте PDF. Попробуйте снова.',
        assessmentError: 'Ошибка при оценке. Попробуйте снова.'
      };
    default:
      return {
        pdfSuccess: 'PDF successfully generated. Check the exports folder.',
        pdfError: 'Error exporting PDF. Please try again.',
        assessmentError: 'Assessment error. Please try again.'
      };
  }
};
