task_system_prompt: str = '''You are an AI designed to provide the most helpful, clear, and concise responses. Focus on giving actionable information, ensuring accuracy and detail without overwhelming the user. You should also be patient, polite, and calm. Avoid unnecessary complexity and always prioritize practical, user-friendly advice. '''

task_prompt_tempalte: str = """Background: '''{background}'''
A group of {party_num} political parties in the European Parliament were required to find consensus on this topic:
{topic}
Below is each party's stance:
{stances}
{task_requirements}
Your task is to write a consensus European Parliament resolution statement that meets the upper requirements in one continuous paragraph, without any formatting or line breaks. Begin the resolution statement with 'The European Parliament raised' and focus on the resolution's substantive content, decisions, and numerical data where applicable. When addressing opposing stances, provide detailed solutions and mitigations to address the concerns raised. For supporting stances that need to be moderated, present them with appropriate qualifications and limitations. Omit procedural details like voting records and amendments, focusing only on the original resolution text. Ensure the output is concise yet comprehensive. Here's an example of the resolution: 
'''{resolution}'''
Now is your turn:"""


one_example_resolution: str = """The European Parliament raised the importance of territorial cohesion as a key EU objective under Article 174 of the Treaty on the Functioning of the European Union, emphasizing the need to address severe and permanent natural or demographic challenges faced by mountain regions, islands, and sparsely populated areas. It highlighted shared obstacles such as demographic shifts, accessibility issues, climate change, and energy vulnerabilities, urging tailored development strategies and EU-wide policies to leverage their unique assets while mitigating handicaps. The resolution stressed that GDP should remain the primary criterion for regional funding eligibility but called for supplementary indicators (e.g., population density, unemployment rates) to better assess regional disparities. It advocated for a flexible, integrated EU policy framework with legal and financial measures, including Structural Funds, Cohesion Fund, and European Investment Bank instruments, to enhance competitiveness and sustainable development. The Parliament urged Member States and regional authorities to adopt a subsidiarity-based approach, aligning with EU2020 goals in energy, R&D, and territorial cooperation, and recommended revising cross-border cooperation criteria—such as eliminating the 150 km maritime distance rule for islands—to foster regional integration. It also emphasized continued financial support for these regions in future EU budgets and promoted the use of European Groupings of Territorial Cooperation (EGTCs) to strengthen cross-border projects and connectivity."""


opinion_prompt_template: str = """Party {party_name}: '''{stance}'''"""

task_requirement_templates = {
    "seat_apportionment": """The resolution should be based on the seat proportions of each party, where the proportions are defined by the following weights rather than actual parliamentary seats:\n{seat_apportionment_weights}""",
    "rawlsianism": "The resolution should be based on the Rawlsianism principle, which means maximizing the benefits for the political parties with the weakest positions to achieve the greatest possible fairness.",
    "utilitarianism": "The resolution should be based on the Utilitarianism principle, which means maximizing the preferences of all political parties while ensuring their sum is maximized."
}

seat_apportionment_weight_template: str = """Party {party_name}'s seat porpotion is {seat_proportion}%."""

voting_requirement_templates = {
    "simple_majority": "The resolution should be supported by more than 50% of the parliament members. The resolution should reflect each party's stance in proportion to their seat allocation.",
    "2_3_majority": "The resolution should be supported by more than two-thirds of the parliament members. The resolution should reflect each party's stance in proportion to their seat allocation.",
    "veto_power": "Because of {veto_party_name} has veto power, the resolution should meet the stances of {veto_party_name} as much as possbile while also be supported by more than 50% of the parliament members. The resolution should reflect each party's stance in proportion to their seat allocation.",
    "none": "The resolution should reflect each party's stance in proportion to their seat allocation."
}
