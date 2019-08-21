package com.onlinebanking.utility;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.Map;

public class EmailTemplate {

    private String templateId;

    private String template;

    private Map<String, String> replacementParams;

    public EmailTemplate(String templateId) {
        this.templateId = templateId;
        this.template = "Hi {{user}}\n" +
                "\n" +
                "Your Otp Number is {{otpnum}}\n" +
                "\n" +
                "Thanks,\n";
    }

    private String loadTemplate(String templateId) throws Exception {
        ClassLoader classLoader = getClass().getClassLoader();
        String path = classLoader.getResource(templateId).getFile().replace("!", "");
        File file = new File(path);
        System.out.println(path);

        System.out.println("File Found : " + file.exists());
        String content = "Empty";
        try {
            content = new String(Files.readAllBytes(file.toPath()));
        } catch (IOException e) {
            throw new Exception("Could not read template with ID = " + templateId);
        }
        return content;
    }

    public String getTemplate(Map<String, String> replacements) {
        String cTemplate = this.template;

        //Replace the String
        for (Map.Entry<String, String> entry : replacements.entrySet()) {
            cTemplate = cTemplate.replace("{{" + entry.getKey() + "}}", entry.getValue());
        }
        return cTemplate;
    }
}
