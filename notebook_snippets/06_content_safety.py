# %% Moderate a learner question with Azure AI Content Safety.
from course_knowledge.safety import ContentSafetyGate
from course_knowledge.settings import content_safety_settings

print(ContentSafetyGate.from_settings(content_safety_settings()).assess("Explain GraphRAG simply."))
