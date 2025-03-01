from django.db import models
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from .helper import generate_code

# Validators
letters_only_validator = RegexValidator(
    regex=r'^[A-Za-z]+$',
    message='This field must contain only letters (no spaces).'
)

words_validator = RegexValidator(
    regex=r'^[A-Za-z\s]+$',
    message='This field must contain only letters and spaces.'
)

# Validator for fields that allow numbers, letters, spaces, and apostrophes (no accents)
allowed_chars_validator = RegexValidator(
    regex=r'^[0-9A-Za-z\'\s]+$',
    message="Only numbers, letters, spaces and apostrophes are allowed. Accents are not allowed."
)

# Validator for names: letters, numbers, apostrophes, and spaces allowed (no accents)
name_validator = RegexValidator(
    regex=r'^[0-9A-Za-z\s\']+$',
    message="Only letters, numbers, spaces, and apostrophes are allowed. Accents are not allowed."
)


###########################################################################################
# COVER QUESTIONNAIRE MODEL
###########################################################################################

class Cover_tbl(models.Model):
    enumerator_name = models.CharField(
        max_length=100,
        # validators=[letters_only_validator],
        help_text="Enumerator name (letters only, no spaces)."
    )
    enumerator_code = models.CharField(max_length=50, blank=True, unique=True)
    # country = models.CharField(max_length=100)
    country = models.CharField(
        max_length=100,
        validators=[letters_only_validator],
        help_text="Should contain only letters."
    )
    # region = models.CharField(max_length=100)
    region = models.CharField(
        max_length=100,
        validators=[letters_only_validator],
        help_text="Should contain only letters."
    )
    # district = models.CharField(max_length=100)
    district = models.CharField(
        max_length=100,
        validators=[letters_only_validator],
        help_text="Should contain only letters."
    )
    
    society = models.CharField(max_length=100)
    society_code = models.CharField(max_length=50, blank=True, unique=True)
    farmer_code = models.CharField(max_length=50, blank=True, unique=True)
    farmer_surname = models.CharField(
        max_length=100,
        validators=[words_validator],
        help_text="Farmer surname (letters and spaces only)."
    )
    
    farmer_first_name = models.CharField(
        max_length=100,
        validators=[words_validator],
        help_text="Farmer first name (letters and spaces only)."
    )
    
    risk_classification = models.CharField(max_length=50)
    client = models.CharField(max_length=50)
    num_farmer_children = models.IntegerField(
        verbose_name="Number of farmer children aged 5-17 captured in Household"
    )
    
    list_children = models.TextField(
        verbose_name="List of children aged 5 to 17 captured in Household",
        blank=True,
        help_text="Enter names or details as a comma-separated list."
    )
    def save(self, *args, **kwargs):
        # Auto-generate farmer_code if not provided using farmer_name.
        if not self.farmer_code and self.farmer_first_name:
            self.farmer_code = generate_code(self.farmer_first_name, prefix="FARM")
        # Auto-generate enumerator_code if not provided using enumerator_name.
        if not self.enumerator_code and self.enumerator_name:
            self.enumerator_code = generate_code(self.enumerator_name, prefix="ENUM")
        # Auto-generate society_code if not provided using society.
        if not self.society_code and self.society:
            self.society_code = generate_code(self.society, prefix="SOC")
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.enumerator_name} - {self.farmer_code}"


    ###########################################################################################
    # CONSENT AND LOCATION MODEL
    ###########################################################################################

class ConsentLocation_tbl(models.Model):
    
    cover = models.OneToOneField(
        Cover_tbl,
        on_delete=models.CASCADE,
        related_name='consent_location',
        null=True
    )
    
    interview_start_time = models.DateTimeField(
        verbose_name="Interview Start/Pick-up Time"
    )
    
    gps_point = models.CharField(
        max_length=100,
        verbose_name="GPS Point of the Household"
    )
    
    # Community type with explicit choices
    COMMUNITY_CHOICES = [
        ('Town', 'Town'),
        ('Village', 'Village'),
        ('Camp', 'Camp'),
    ]
    community_type = models.CharField(
        max_length=20,
        choices=COMMUNITY_CHOICES,
        verbose_name="Type of Community"
    )

    # Does the farmer reside in the community stated on the cover?
    RESIDE_IN_COMMUNITY = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    farmer_resides_in_community = models.CharField(
        null=False,
        blank=False,
        choices=RESIDE_IN_COMMUNITY,
        verbose_name="Does the farmer reside in the community stated on the cover?"
    )

    # If No, provide the name of the community the farmer resides in.
    # This field expects capital letters and numbers only.
    community_name_validator = RegexValidator(
        regex=r'^[A-Z0-9]+$',
        message="Community name must be in capital letters without any special characters."
    )
    
    community_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="If the farmer does NOT reside in the cover community, provide the community name here.",
        validators=[community_name_validator]
    )

    farmer_community = models.CharField(
        max_length=100,
        blank=True,
        help_text="If the farmer does NOT reside in the cover community, provide the community name here.",
        validators=[community_name_validator]
    )

    # Is the farmer available?
    YES_OR_NO = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    farmer_available = models.CharField(
        null=True,
        blank=True,
        choices=YES_OR_NO,
        verbose_name="Is the farmer available?"
    )

    # If No, for what reason? Use defined choices.
    UNAVAILABLE_REASON_CHOICES = [
        ('Non-resident', 'Non-resident'),
        ('Deceased', 'Deceased'),
        ("Doesn't work with TOUTON anymore", "Doesn't work with TOUTON anymore"),
        ('Other', 'Other'),
    ]
    reason_unavailable = models.CharField(
        max_length=50,
        choices=UNAVAILABLE_REASON_CHOICES,
        blank=True,
        help_text="If the farmer is not available, select the reason."
    )

    reason_unavailable_other = models.CharField(
        max_length=100,
        blank=True,
        help_text="If the farmer is not available, provide the reason here."
    )
    # Who is available to answer for the farmer?
    ANSWER_BY_CHOICES = [
        ('Caretaker', 'Caretaker'),
        ('Spouse', 'Spouse'),
        ('Nobody', 'Nobody'),
    ]
    available_answer_by = models.CharField(
        max_length=20,
        choices=ANSWER_BY_CHOICES,
        blank=True,
        help_text="Who is available to answer for the farmer?"
    )
        
        
        
    #################################################################################
    #FARMER IDENTIFICATION
    #################################################################################
    
class FarmerIdentificationtbl(models.Model):

    CORRECT_RESPONSE_PROVIDED = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    # Name verification
    cover = models.OneToOneField(
        Cover_tbl,
        on_delete=models.CASCADE,
        related_name='farmer_identification',
        null=True
    )
     
    is_name_correct = models.CharField(
        choices = CORRECT_RESPONSE_PROVIDED,
        verbose_name="Is the name of the respondent correct?",
        help_text="If 'No', please fill in the exact name and surname of the producer."
    )
    exact_name = models.CharField(
        max_length=200,
        blank=True,
        validators=[allowed_chars_validator],
        help_text="Exact name and surname of the producer (if respondent name is incorrect)."
    )

    # Nationality and country of origin
    NATIONALITY_CHOICES = [
        ('Ghanaian', 'Ghanaian'),
        ('Non Ghanaian', 'Non Ghanaian'),
    ]
    nationality = models.CharField(
        max_length=20,
        choices=NATIONALITY_CHOICES,
        verbose_name="Nationality of the respondent"
    )

    COUNTRY_ORIGIN_CHOICES = [
        ('Burkina Faso', 'Burkina Faso'),
        ('Mali', 'Mali'),
        ('Guinea', 'Guinea'),
        ('Ivory Coast', 'Ivory Coast'),
        ('Liberia', 'Liberia'),
        ('Togo', 'Togo'),
        ('Benin', 'Benin'),
        ('Niger', 'Niger'),
        ('Nigeria', 'Nigeria'),
        ('Other', 'Other'),
    ]
    country_origin = models.CharField(
        max_length=50,
        choices=COUNTRY_ORIGIN_CHOICES,
        blank=True,
        help_text="If Non Ghanaian, select the country of origin."
    )
    country_origin_other = models.CharField(
        max_length=100,
        blank=True,
        help_text="If 'Other' is selected, please specify the country of origin."
    )

    # Ownership information
    CORRECT_RESPONSE_PROVIDED = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    is_owner = models.CharField(
        choices = CORRECT_RESPONSE_PROVIDED,
        verbose_name="Is the respondent the owner of the farm?",
        help_text="If 'No', please fill in the farm's name and details."
    )

    OWNER_STATUS_CHOICES = [
        ('Complete Owner', 'Complete Owner'),
        ('Sharecropper', 'Sharecropper'),
        ('Owner/Sharecropper', 'Owner/Sharecropper'),
    ]
    owner_status_01 = models.CharField(
        max_length=30,
        choices=OWNER_STATUS_CHOICES,
        blank=True,
        help_text="Which of these best describes you?"
    )

    OWNER_STATUS_CHOICES = [
        ('Coaretaker/Manager of the farm', 'Coaretaker/Manager of the farm'),
        ('Sharecropper', 'Sharecropper'),
    ]
    owner_status_00 = models.CharField(
        max_length=30,
        choices=OWNER_STATUS_CHOICES,
        blank=True,
        help_text="Which of these best describes you?"
    )



    #################################################################################
    #OWNER IDENTIFICATION
    #################################################################################

    
class OwnerIdentificationTbl(models.Model):
    
    cover = models.OneToOneField(
        Cover_tbl,
        on_delete=models.CASCADE,
        related_name='owner_identification',
        null=True
    )

    owner_name_validator = RegexValidator(
        regex=r'^[A-Za-z\']+$',
        message="This field must contain only letters and apostrophes (no spaces or accents)."
    )

    name_owner = models.CharField(
        max_length=100,
        validators=[owner_name_validator],
        verbose_name="Owner's Last Name",
        blank=True,
        help_text="Enter the owner's surname. Letters and apostrophes only (no spaces or accents)."
    )
    first_name_owner = models.CharField(
        max_length=100,
        validators=[owner_name_validator],
        verbose_name="Owner's First Name",
        blank=True,
        help_text="Enter the owner's first name. Letters and apostrophes only (no spaces or accents)."
    )

    # Nationality of the owner
    NATIONALITY_OWNER_CHOICES = [
        ('Ghanaian', 'Ghanaian'),
        ('Non Ghanaian', 'Non Ghanaian'),
    ]
    nationality_owner = models.CharField(
        max_length=20,
        choices=NATIONALITY_OWNER_CHOICES,
        verbose_name="What is the nationality of the owner?"
    )

    # Country of origin of the owner (if Non Ghanaian)
    COUNTRY_ORIGIN_OWNER_CHOICES = [
        ('Burkina Faso', 'Burkina Faso'),
        ('Mali', 'Mali'),
        ('Guinea', 'Guinea'),
        ('Ivory Coast', 'Ivory Coast'),
        ('Liberia', 'Liberia'),
        ('Togo', 'Togo'),
        ('Benin', 'Benin'),
        ('Other', 'Other'),
    ]
    country_origin_owner = models.CharField(
        max_length=200,
        choices=COUNTRY_ORIGIN_OWNER_CHOICES,
        blank=True,
        verbose_name="Country of origin of the owner",
        help_text="If the owner is Non Ghanaian, select the country of origin."
    )
    country_origin_owner_other = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Specify country of origin (if Other)",
        help_text="If 'Other' is selected above, please specify the country."
    )

    # Manager work length: number of years the respondent has been working for the owner.
    manager_work_length = models.IntegerField(
        verbose_name="For how many years has the respondent been working for the owner?"
    )


    #################################################################################
    # WORKERS IN THE FARM
    #################################################################################
    # A simple yes/no choice coded as "01" for Agree and "02" for Disagree.\
        
class WorkerInTheFarmTbl(models.Model):
    
    cover = models.OneToOneField(
        Cover_tbl,
        on_delete=models.CASCADE,
        related_name='worker_in_farm',
        null=True
    )
    
    YES_NO_CHOICES = [
        ('01', 'Agree'),
        ('02', 'Disagree'),
    ]

    # For the worker agreement type, we allow an "Other" option requiring specification.
    WORKER_AGREEMENT_CHOICES = [
        ('VerbalWithoutWitness', 'Verbal agreement without witness'),
        ('VerbalWithWitness', 'Verbal agreement with witness'),
        ('WrittenWithoutWitness', 'Written agreement without witness'),
        ('WrittenWithWitness', 'Written contract with witness'),
        ('Other', 'Other'),
    ]

    # For the type of worker recruitment.
    WORKER_RECRUITMENT_CHOICES = [
        ('Permanent', 'Permanent labor'),
        ('Casual', 'Casual labor'),
    ]

    # For salary status.
    SALARY_STATUS_CHOICES = [
        ('Always', 'Always'),
        ('Sometimes', 'Sometimes'),
        ('Rarely', 'Rarely'),
        ('Never', 'Never'),
    ]
    
    REFUSAL_ACTION_CHOICES = [
            ('Compromise', 'I find a compromise'),
            ('SalaryDeduction', 'I withdraw part of their salary'),
            ('Warning', 'I issue a warning'),
            ('Other', 'Other'),
            ('NotApplicable', 'Not applicable'),
        ]


    # Recruitment questions
    recruited_workers = models.BooleanField(
        verbose_name="Have you recruited at least one worker during the past year?",
        help_text="Yes or No"
    )
    worker_recruitment_type = models.CharField(
        max_length=10,
        choices=WORKER_RECRUITMENT_CHOICES,
        verbose_name="Do you recruit workers for..."
    )
    
    # Agreement with workers
    worker_agreement_type = models.CharField(
        max_length=30,
        choices=WORKER_AGREEMENT_CHOICES,
        verbose_name="What kind of agreement do you have with your workers?"
    )
    worker_agreement_other = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Specify other agreement type",
        help_text="Provide details if 'Other' is selected."
    )
    
    # Clarification of tasks during recruitment
    tasks_clarified = models.BooleanField(
        verbose_name="Were the tasks to be performed by the worker clarified during recruitment?",
        help_text="Yes or No"
    )
    
    # Additional tasks performed outside the agreement
    additional_tasks = models.BooleanField(
        verbose_name="Does the worker perform tasks for you or your family members other than those agreed upon?",
        help_text="Yes or No"
    )
    
    # Refusal to perform tasks

    refusal_action = models.CharField(
        max_length=20,
        choices=REFUSAL_ACTION_CHOICES,
        verbose_name="What do you do when a worker refuses to perform a task?"
    )
    refusal_action_other = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Specify refusal action",
        help_text="Fill this if 'Other' is selected."
    )
    
    # Salary status of workers
    salary_status = models.CharField(
        max_length=10,
        choices=SALARY_STATUS_CHOICES,
        verbose_name="Do your workers receive their full salaries?"
    )
    
    # Attitudinal statements: Using yes/no choices
    recruit_1 = models.CharField(
        max_length=2,
        choices=YES_NO_CHOICES,
        verbose_name="It is acceptable for a person who cannot pay their debts to work for the creditor to reimburse the debt."
    )
    recruit_2 = models.CharField(
        max_length=2,
        choices=YES_NO_CHOICES,
        verbose_name="It is acceptable for an employer not to reveal the true nature of the work during recruitment."
    )
    recruit_3 = models.CharField(
        max_length=2,
        choices=YES_NO_CHOICES,
        verbose_name="A worker is obliged to work whenever he is called upon by his employer."
    )
    conditions_1 = models.CharField(
        max_length=2,
        choices=YES_NO_CHOICES,
        verbose_name="A worker is not entitled to move freely."
    )
    conditions_2 = models.CharField(
        max_length=2,
        choices=YES_NO_CHOICES,
        verbose_name="A worker must be free to communicate with his or her family and friends."
    )
    conditions_3 = models.CharField(
        max_length=2,
        choices=YES_NO_CHOICES,
        verbose_name="A worker is obliged to adapt to any living conditions imposed by the employer."
    )
    conditions_4 = models.CharField(
        max_length=2,
        choices=YES_NO_CHOICES,
        verbose_name="It is acceptable for an employer and their family to interfere in a worker's private life."
    )
    conditions_5 = models.CharField(
        max_length=2,
        choices=YES_NO_CHOICES,
        verbose_name="A worker should not have the freedom to leave work whenever they wish."
    )
    leaving_1 = models.CharField(
        max_length=2,
        choices=YES_NO_CHOICES,
        verbose_name="A worker should be required to stay longer than expected while waiting for unpaid salary."
    )
    leaving_2 = models.CharField(
        max_length=2,
        choices=YES_NO_CHOICES,
        verbose_name="A worker should not be able to leave their employer when they owe money to their employer."
    )
    
    # Attitudinal statement regarding recruitment ethics
    consent_recruitment = models.CharField(
        max_length=2,
        choices=YES_NO_CHOICES,
        verbose_name="It is acceptable to recruit someone for work without their consent."
    )
    


    #################################################################################
    # ADULT OF THE RESPONDENTS HOUSEHOLD
    #################################################################################
    
class AdultInHouseholdTbl(models.Model):

    cover = models.OneToOneField(
        Cover_tbl,
        on_delete=models.CASCADE,
        related_name='adult_in_household',
        null=True
    )
    
    total_adults = models.PositiveIntegerField(
            verbose_name="Total number of adults in the household (producer/manager/owner not included)",
            help_text="Household means people that dwell under the same roof and share the same meal."
        )
    # An ArrayField to store a list of full names
    full_names = ArrayField(
        models.CharField(max_length=200, validators=[name_validator]),
        verbose_name="List of full names of household members",
        help_text="Enter each household member's full name. Characters with accents are not allowed.",
        default=list,
        blank=True
        )

    # Relationship of this member to the respondent (producer/manager/owner)
    RELATIONSHIP_CHOICES = [
        ('Husband/Wife', 'Husband/Wife'),
        ('Son/Daughter', 'Son/Daughter'),
        ('Brother/Sister', 'Brother/Sister'),
        ('Son-in-law/Daughter-in-law', 'Son-in-law/Daughter-in-law'),
        ('Grandson/Granddaughter', 'Grandson/Granddaughter'),
        ('Niece/Nephew', 'Niece/Nephew'),
        ('Cousin', 'Cousin'),
        ("Worker's Family", "Worker's Family"),
        ('Worker', 'Worker'),
        ('Father/Mother', 'Father/Mother'),
        ('Other', 'Other (specify)')
    ]
    relationship = models.CharField(
        max_length=50,
        choices=RELATIONSHIP_CHOICES,
        verbose_name="Relationship to the respondent"
    )
    relationship_other = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Specify relationship (if Other)",
        help_text="If 'Other' is selected, please specify."
    )

    # Gender of the household member
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        verbose_name="Gender"
    )

    # Nationality and country of origin
    NATIONALITY_CHOICES = [
        ('Ghanaian', 'Ghanaian'),
        ('Non Ghanaian', 'Non Ghanaian'),
    ]
    nationality = models.CharField(
        max_length=20,
        choices=NATIONALITY_CHOICES,
        verbose_name="Nationality"
    )
    # Country of origin if Non Ghanaian
    COUNTRY_ORIGIN_CHOICES = [
        ('Burkina Faso', 'Burkina Faso'),
        ('Mali', 'Mali'),
        ('Guinea', 'Guinea'),
        ('Ivory Coast', 'Ivory Coast'),
        ('Liberia', 'Liberia'),
        ('Togo', 'Togo'),
        ('Benin', 'Benin'),
        ('Niger', 'Niger'),
        ('Nigeria', 'Nigeria'),
        ('Other', 'Other (specify)')
    ]
    country_origin = models.CharField(
        max_length=50,
        choices=COUNTRY_ORIGIN_CHOICES,
        blank=True,
        verbose_name="Country of origin (if Non Ghanaian)"
    )
    country_origin_other = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Specify country of origin (if Other)"
    )

    # Year of birth, must be between 1910 and 2007
    year_birth = models.IntegerField(
        verbose_name="Year of birth",
    )

    # Whether the household member has a birth certificate
    BIRTH_CERTIFICATE_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    birth_certificate = models.CharField(
        max_length=3,
        choices=BIRTH_CERTIFICATE_CHOICES,
        verbose_name="Does this member have a birth certificate?"
    )

    # Main work/occupation
    MAIN_WORK_CHOICES = [
        ('Farmer_cocoa', 'Farmer (cocoa)'),
        ('Farmer_coffee', 'Farmer (coffee)'),
        ('Farmer_other', 'Farmer (other)'),
        ('Merchant', 'Merchant'),
        ('Student', 'Student'),
        ('Other', 'Other'),
        ('No_activity', 'No activity'),
    ]
    main_work = models.CharField(
        max_length=30,
        choices=MAIN_WORK_CHOICES,
        verbose_name="Main work/occupation"
    )
    main_work_other = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Specify main work (if Other)",
        help_text="If 'Other' is selected, please specify."
    )



    #################################################################################
    # CHILDREN IN THE RESPONDENT'S HOUSEHOLD MODEL
    #################################################################################

class ChildInHouseholdTbl(models.Model):
    # Validator for names: letters and spaces only.
    words_validator = RegexValidator(
        regex=r'^[A-Za-z\s]+$',
        message='This field must contain only letters and spaces.'
    )

    # Validator for fields that must be in capital letters and numbers (no accents)
    capital_letters_numbers_validator = RegexValidator(
        regex=r'^[A-Z0-9\s]+$',
        message="Only capital letters, numbers, and spaces are allowed."
    )

    cover = models.OneToOneField(
        Cover_tbl,
        on_delete=models.CASCADE,
        related_name='child_in_household',
        null=True
    )
    
    # Choices for who is answering when the child is not available.
    WHO_ANSWERS_CHOICES = [
        ('parents', 'The parents or legal guardians'),
        ('family_member', 'Another family member'),
        ('sibling', "One of the child's siblings"),
        ('other', 'Other'),
    ]

    # Gender choices
    GENDER_CHOICES = [
        ('Boy', 'Boy'),
        ('Girl', 'Girl'),
    ]

    # Choices for birth certificate
    BIRTH_CERTIFICATE_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    # Choices for Yes/No questions (you can adjust the codes if needed)
    YES_NO_CHOICES = [
        ('01', 'Yes'),
        ('02', 'No'),
    ]

    # Choices for the unavailability reasons when a child cannot be surveyed.
    CHILD_UNAVAILABILITY_REASON_CHOICES = [
        ('school', 'The child is at school'),
        ('work_cocoa', 'The child has gone to work on the cocoa farm'),
        ('housework', 'Child is busy doing housework'),
        ('work_outside', 'Child works outside the household'),
        ('too_young', 'The child is too young'),
        ('sick', 'The child is sick'),
        ('travelled', 'The child has travelled'),
        ('play', 'The child has gone out to play'),
        ('sleeping', 'The child is sleeping'),
        ('other', 'Other reasons'),
    ]



    # Aggregated household information
    children_present = models.BooleanField(
        verbose_name="Are there children living in the respondent's household?",
        help_text="Answer Yes if there are children, No otherwise."
    )
    num_children_5_to_17 = models.PositiveSmallIntegerField(
        verbose_name="Number of children between ages 5 and 17",
        validators=[MinValueValidator(1), MaxValueValidator(19)],
        help_text="Count the producer's children as well as other children living in the household (cannot be negative or exceed 19)."
    )

    # Information for the specific child (from the cover) being surveyed
    child_declared_in_cover = models.BooleanField(
        verbose_name="Is the child among those declared in the cover as the farmer's child?",
        help_text="Yes if the child is already listed in the cover; No otherwise."
    )
    child_identifier = models.PositiveSmallIntegerField(
        verbose_name="Child identifier",
        validators=[MinValueValidator(1), MaxValueValidator(19)],
        help_text="Enter the number attached to the child's name in the cover (must be less than 20)."
    )

    child_can_be_surveyed = models.BooleanField(
        verbose_name="Can the child be surveyed now?",
        help_text="Answer Yes if the child is available for survey; No otherwise."
    )
    child_unavailability_reason = models.CharField(
        max_length=20,
        choices=CHILD_UNAVAILABILITY_REASON_CHOICES,
        blank=True,
        verbose_name="Reason for child not being surveyed",
        help_text="Select the reason if the child cannot be surveyed."
    )

        

    # If the child is not available, capture additional reasons.
    child_not_avail = models.CharField(
        max_length=200,
        blank=True,
        validators=[capital_letters_numbers_validator],
        verbose_name="Other reasons (in capital letters) for child not being available",
        help_text="Provide reasons in capital letters. (Minimum length can be validated separately.)"
    )

    # Who is answering for the child when the child is not available.
    who_answers_child_unavailable = models.CharField(
        max_length=20,
        choices=WHO_ANSWERS_CHOICES,
        blank=True,
        verbose_name="Who is answering for the child (if not available)"
    )
    who_answers_child_unavailable_other = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Specify who is answering (if Other is selected)"
    )

    # Child's identification fields.
    child_first_name = models.CharField(
        max_length=100,
        validators=[words_validator],
        verbose_name="Child's First Name"
    )
    child_surname = models.CharField(
        max_length=100,
        validators=[words_validator],
        verbose_name="Child's Surname"
    )

    child_gender = models.CharField(
        max_length=4,
        choices=GENDER_CHOICES,
        verbose_name="Gender of the Child"
    )

    child_year_birth = models.IntegerField(
        verbose_name="Year of Birth of the Child",
        validators=[MinValueValidator(2007), MaxValueValidator(2020)],
        help_text="The year must be between 2007 and 2020 (child must be between 5 and 17 years old)."
    )

    child_birth_certificate = models.CharField(
        max_length=3,
        choices=BIRTH_CERTIFICATE_CHOICES,
        verbose_name="Does the child have a birth certificate?"
    )
    child_birth_certificate_reason = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="If no, please specify why",
        help_text="Provide a reason if the child does not have a birth certificate."
    )

    # --- Validators ---
    # Validator to ensure names are in capital letters and numbers only (no accents)
    capital_letters_numbers_validator = RegexValidator(
        regex=r'^[A-Z0-9\s]+$',
        message="Only capital letters, numbers, and spaces are allowed."
    )

    # --- Choice definitions ---

    # Child born in community choices
    CHILD_BORN_CHOICES = [
        ('Yes', 'Yes'),
        ('DiffComm', 'No, born in this district but different community'),
        ('DiffDist', 'No, born in this region but different district'),
        ('DiffReg', 'No, born in another region of Ghana'),
        ('AnotherCountry', 'No, born in another country'),
    ]

    # Country of birth (if not born in the cover community)
    COUNTRY_OF_BIRTH_CHOICES = [
        ('Benin', 'Benin'),
        ('BurkinaFaso', 'Burkina Faso'),
        ('IvoryCoast', 'Ivory Coast'),
        ('Mali', 'Mali'),
        ('Niger', 'Niger'),
        ('Togo', 'Togo'),
        ('Other', 'Other'),
    ]

    # Relationship to head of household
    CHILD_RELATIONSHIP_CHOICES = [
        ('Son/Daughter', 'Son/Daughter'),
        ('Brother/Sister', 'Brother/Sister'),
        ('SonInLaw/DaughterInLaw', 'Son-in-law/Daughter-in-law'),
        ('Grandson/Granddaughter', 'Grandson/Granddaughter'),
        ('Niece/Nephew', 'Niece/nephew'),
        ('Cousin', 'Cousin'),
        ('ChildOfWorker', "Child of the worker"),
        ('ChildOfOwner', "Child of the farm owner"),
        ('Other', 'Other'),
    ]

    # Reasons for not living with family
    CHILD_NOT_LIVE_REASONS = [
        ('ParentsDeceased', 'Parents deceased'),
        ('CantCare', "Can't take care of me"),
        ('Abandoned', 'Abandoned'),
        ('SchoolReasons', 'School reasons'),
        ('AgencyBrought', 'A recruitment agency brought me here'),
        ('DidNotWant', 'I did not want to live with my parents'),
        ('Other', 'Other'),
    ]

    # Who decided that the child comes into the household
    CHILD_DECISION_MAKER_CHOICES = [
        ('Myself', 'Myself'),
        ('Parents', 'Father/Mother'),
        ('Grandparents', 'Grandparents'),
        ('OtherFamily', 'Other family members'),
        ('External', 'External recruiter/agency'),
        ('Other', 'Other person'),
    ]

    # Child agreement with decision (Yes/No)
    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    # Last time child saw parents
    LAST_SEEN_CHOICES = [
        ('1week', 'Max 1 week'),
        ('1month', 'Max 1 month'),
        ('1year', 'Max 1 year'),
        ('MoreThan1year', 'More than 1 year'),
        ('Never', 'Never'),
    ]

    # Duration of living in the household
    LIVING_DURATION_CHOICES = [
        ('Born', 'Born in the household'),
        ('Less1', 'Less than 1 year'),
        ('1-2', '1-2 years'),
        ('2-4', '2-4 years'),
        ('4-6', '4-6 years'),
        ('6-8', '6-8 years'),
        ('More8', 'More than 8 years'),
        ('DontKnow', "Don't know"),
    ]

    # Who accompanied the child to come here
    CHILD_ACCOMPANIED_CHOICES = [
        ('Alone', 'Came alone'),
        ('Parents', 'Father/Mother'),
        ('Grandparents', 'Grandparents'),
        ('OtherFamily', 'Other family member'),
        ('WithRecruit', 'With a recruit'),
        ('Other', 'Other'),
    ]

    ############################################
    # ChildHouseholdDetails Model
    ############################################


    # 1. Community of birth
    child_born_in_community = models.CharField(
        max_length=20,
        choices=CHILD_BORN_CHOICES,
        verbose_name="Is the child born in this community?",
        help_text="Select an option."
    )
    child_country_of_birth = models.CharField(
        max_length=20,
        choices=COUNTRY_OF_BIRTH_CHOICES,
        blank=True,
        verbose_name="In which country is the child born?",
        help_text="Provide this only if 'No, born in another country' is selected."
    )
    child_country_of_birth_other = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Specify country of birth (if Other)",
        help_text="Use capital letters without special characters.",
        validators=[capital_letters_numbers_validator]
    )
    
    # 2. Relationship to the head of household
    child_relationship_to_head = models.CharField(
        max_length=50,
        choices=CHILD_RELATIONSHIP_CHOICES,
        verbose_name="Relationship of the child to the head of the household"
    )
    child_relationship_to_head_other = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Specify relationship (if Other)",
        help_text="Write in capital letters without special characters.",
        validators=[capital_letters_numbers_validator]
    )
    
    # 3. Reason for not living with family (if applicable)
    child_not_live_with_family_reason = models.CharField(
        max_length=50,
        choices=CHILD_NOT_LIVE_REASONS,
        blank=True,
        verbose_name="Why does the child not live with his/her family?"
    )
    child_not_live_with_family_reason_other = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Other reason (if Other is selected)"
    )
    
    # 4. Decision-maker for child's presence in household
    child_decision_maker = models.CharField(
        max_length=30,
        choices=CHILD_DECISION_MAKER_CHOICES,
        verbose_name="Who decided that the child comes into the household?"
    )
    child_decision_maker_other = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Specify decision maker (if Other is selected)"
    )
    
    # 5. Did the child agree with the decision?
    child_agree_with_decision = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        verbose_name="Did the child agree with this decision?"
    )
    
    # 6. Parent contact: Has the child seen/spoken with parents in the past year?
    child_seen_parents = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        verbose_name="Has the child seen and/or spoken with his/her parents in the past year?"
    )
    child_last_seen_parent = models.CharField(
        max_length=20,
        choices=LAST_SEEN_CHOICES,
        verbose_name="When was the last time the child saw/talked with a parent?"
    )
    
    # 7. Duration of child's residence in the household
    child_living_duration = models.CharField(
        max_length=20,
        choices=LIVING_DURATION_CHOICES,
        verbose_name="For how long has the child been living in the household?"
    )
    
    # 8. Who accompanied the child to come here?
    child_accompanied_by = models.CharField(
        max_length=20,
        choices=CHILD_ACCOMPANIED_CHOICES,
        verbose_name="Who accompanied the child to come here?"
    )
    child_accompanied_by_other = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Specify accompaniment (if Other is selected)"
    )
    

        ############################################
        # ChildEducationDetails Model   
        ############################################

    # --- Father-related fields ---
    FATHER_LOCATION_CHOICES = [
        ('same_household', 'In the same household'),
        ('another_household_village', 'In another household in the same village'),
        ('another_household_region', 'In another household in the same region'),
        ('another_household_other_region', 'In another household in another region'),
        ('abroad', 'Abroad'),
        ('parents_deceased', 'Parents deceased'),
        ('dont_know', "Don't know/Don't want to answer"),
    ]
    COUNTRY_CHOICES = [
        ('Benin', 'Benin'),
        ('Burkina Faso', 'Burkina Faso'),
        ('Ghana', 'Ghana'),
        ('Guinea', 'Guinea'),
        ('Guinea-Bissau', 'Guinea-Bissau'),
        ('Liberia', 'Liberia'),
        ('Mauritania', 'Mauritania'),
        ('Mali', 'Mali'),
        ('Nigeria', 'Nigeria'),
        ('Niger', 'Niger'),
        ('Senegal', 'Senegal'),
        ('Sierra Leone', 'Sierra Leone'),
        ('Togo', 'Togo'),
        ('dont_know', "Don't know"),
        ('other', "Other"),
    ]
    child_father_location = models.CharField(
        max_length=50,
        choices=FATHER_LOCATION_CHOICES,
        null=True,
        blank=True,
        help_text="Where does the child's father live?"
    )
    child_father_country = models.CharField(
        max_length=50,
        choices=COUNTRY_CHOICES,
        null=True,
        blank=True,
        help_text="Father's country of residence."
    )
    child_father_country_other = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="If 'Other' is selected, specify the country (in capital letters)."
    )
    
    # --- Mother-related fields ---
    # (Using the same location choices as father)
    child_mother_location = models.CharField(
        max_length=50,
        choices=FATHER_LOCATION_CHOICES,
        null=True,
        blank=True,
        help_text="Where does the child's mother live?"
    )
    child_mother_country = models.CharField(
        max_length=50,
        choices=COUNTRY_CHOICES,
        null=True,
        blank=True,
        help_text="Mother's country of residence."
    )
    child_mother_country_other = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="If 'Other' is selected, specify the country (in capital letters)."
    )
    
    # --- Schooling and Education fields ---
    # Whether the child is currently enrolled in school:
    EDUCATION_STATUS_CHOICES = [
        (1, 'Yes'),
        (0, 'No'),
    ]
    child_educated = models.IntegerField(
        choices=EDUCATION_STATUS_CHOICES,
        help_text="Is the child currently enrolled in school? (1 = Yes, 0 = No)"
    )
    child_school_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="Name of the school (if enrolled)."
    )
    SCHOOL_TYPE_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    school_type = models.CharField(
        max_length=20,
        choices=SCHOOL_TYPE_CHOICES,
        null=True,
        blank=True,
        help_text="Is the school public or private?"
    )
    # Child's grade enrollment choices:
    GRADE_CHOICES = [
        ('K1', 'Kindergarten 1'),
        ('K2', 'Kindergarten 2'),
        ('P1', 'Primary 1'),
        ('P2', 'Primary 2'),
        ('P3', 'Primary 3'),
        ('P4', 'Primary 4'),
        ('P5', 'Primary 5'),
        ('P6', 'Primary 6'),
        ('JHS1', 'JHS/JSS 1'),
        ('JHS2', 'JHS/JSS 2'),
        ('JHS3', 'JHS/JSS 3'),
        ('SSS1', 'SSS/JHS 1'),
        ('SSS2', 'SSS/JHS 2'),
        ('SSS3', 'SSS/JHS 3'),
        ('SSS4', 'SSS/JHS 4'),
    ]
    child_grade = models.CharField(
        max_length=10,
        choices=GRADE_CHOICES,
        null=True,
        blank=True,
        help_text="What grade is the child enrolled in?"
    )
    # How many times the child goes to school in a week:
    SCHOOL_GOING_TIMES_CHOICES = [
        ('01', 'Once'),
        ('02', 'Twice'),
        ('03', 'Thrice'),
        ('04', 'Four times'),
        ('05', 'Five times'),
    ]
    sch_going_times = models.IntegerField(
        choices=SCHOOL_GOING_TIMES_CHOICES,
        null=True,
        blank=True,
        help_text="How many times does the child go to school in a week?"
    )
    # Basic school needs available (multiple choice):
    # Here we store a comma-separated list of selected needs.
    BASIC_NEED_CHOICES = [
        ('books', 'Books'),
        ('bag', 'School bag'),
        ('pen', 'Pen / Pencils'),
        ('uniform', 'School Uniforms'),
        ('shoes', 'Shoes and Socks'),
        ('none', 'None of the above'),
    ]
    basic_need_available = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Comma-separated basic needs available (e.g., books, bag, pen, uniform, shoes, none)."
    )
    # For children not currently enrolled:
    SCHL2_CHOICES = [
        ('01', 'Yes, they went to school but stopped'),
        ('00', 'No, they have never been to school'),
    ]
    child_schl2 = models.IntegerField(
        choices=SCHL2_CHOICES,
        null=True,
        blank=True,
        help_text="Has the child ever been to school (if not currently enrolled)?"
    )
    child_schl_left_age = models.IntegerField(
        null=True,
        blank=True,
        help_text="Which year did the child leave school? (Or the age at which they left)"
    )
    
    # # --- Additional fields used for validations ---
    # child_year_birth = models.IntegerField(
    #     null=True,
    #     blank=True,
    #     help_text="Year of birth of the child."
    # )
    # child_age = models.IntegerField(
    #     null=True,
    #     blank=True,
    #     help_text="Current age of the child."
    # )
    # child_available = models.BooleanField(
    #     default=True,
    #     help_text="Is the child available? (Used in conditional validations)"
    # )


    #################################################################################
    # CHILD EDUCATIONAL ASSESSMENT MODEL
    #################################################################################
    """
    This model captures the educational assessment section of the survey.
    It is linked via a one-to-one relationship with ChildSurvey.
    """
  
    # --- Calculation Task ---
    CALCULATION_RESPONSE_CHOICES = [
        ('both_correct', 'Yes, the child gave the right answer for both calculations'),
        ('one_correct', 'Yes, the child gave the right answer for one calculation'),
        ('wrong', 'No, the child does not know how to answer and gave wrong answers'),
        ('refused', 'The child refuses to try'),
    ]
    calculation_response = models.CharField(
        max_length=20,
        choices=CALCULATION_RESPONSE_CHOICES,
        help_text="Response to the calculation task."
    )

    # --- Reading Assessment ---
    READING_RESPONSE_CHOICES = [
        ('can_read', 'Yes (he/she can read the sentences)'),
        ('simple_text', 'Only the simple text (text 1.)'),
        ('cannot_read', 'No'),
        ('refused', 'The child refuses to try'),
    ]
    reading_response = models.CharField(
        max_length=20,
        choices=READING_RESPONSE_CHOICES,
        help_text="Response to the reading task."
    )

    # --- Writing Assessment ---
    WRITING_RESPONSE_CHOICES = [
        ('can_write_both', 'Yes, he/she can write both sentences'),
        ('simple_text', 'Only the simple text (text 1.)'),
        ('cannot_write', 'No'),
        ('refused', 'The child refuses to try'),
    ]
    writing_response = models.CharField(
        max_length=20,
        choices=WRITING_RESPONSE_CHOICES,
        help_text="Response to the writing task."
    )

    # --- Education Level ---
    EDUCATION_LEVEL_CHOICES = [
        ('pre_school', 'Pre-school (Kindergarten)'),
        ('primary', 'Primary'),
        ('jss', 'JSS/Middle school'),
        ('sss', "SSS/'O'-level/'A'-level (including vocational & technical training)"),
        ('university', 'University or higher'),
        ('not_applicable', 'Not applicable'),
    ]
    education_level = models.CharField(
        max_length=30,
        choices=EDUCATION_LEVEL_CHOICES,
        help_text="What is the education level of the child?"
    )

    # --- Reasons for Leaving School ---
    SCHOOL_LEFT_REASON_CHOICES = [
        ('too_far', 'The school is too far away'),
        ('tuition', 'Tuition fees for private school too high'),
        ('poor_performance', 'Poor academic performance'),
        ('insecurity', 'Insecurity in the area'),
        ('learn_trade', 'To learn a trade'),
        ('early_pregnancy', 'Early pregnancy'),
        ('child_disinterest', 'The child did not want to go to school anymore'),
        ('affordability', "Parents can't afford Teaching and Learning Materials"),
        ('other', 'Other'),
        ('dont_know', "Does not know"),
    ]
    child_schl_left_why = models.CharField(
        max_length=20,
        choices=SCHOOL_LEFT_REASON_CHOICES,
        null=True,
        blank=True,
        help_text="What is the main reason for the child leaving school?"
    )
    child_schl_left_why_other = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="Specify the reason if 'Other' is selected."
    )

    # --- Reasons for Never Attending School ---
    NEVER_SCHOOL_REASON_CHOICES = [
        ('too_far', 'The school is too far away'),
        ('tuition', 'Tuition fees too high'),
        ('too_young', 'Too young to be in school'),
        ('insecurity', 'Insecurity in the region'),
        ('learn_trade', 'To learn a trade (apprenticeship)'),
        ('child_disinterest', "The child doesn't want to go to school"),
        ('affordability', "Parents can't afford TLMs and/or enrollment fees"),
        ('other', 'Other'),
    ]
    child_why_no_school = models.CharField(
        max_length=20,
        choices=NEVER_SCHOOL_REASON_CHOICES,
        null=True,
        blank=True,
        help_text="Why has the child never been to school?"
    )
    child_why_no_school_other = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="Specify the reason if 'Other' is selected."
    )

    # --- School Attendance in the Past 7 Days ---
    SCHOOL_7DAYS_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    child_school_7days = models.CharField(
        max_length=3,
        choices=SCHOOL_7DAYS_CHOICES,
        null=True,
        blank=True,
        help_text="Has the child been to school in the past 7 days?"
    )

    SCHOOL_ABSENCE_REASON_CHOICES = [
        ('holidays', 'It was the holidays'),
        ('sick', 'He/she was sick'),
        ('working', 'He/she was working'),
        ('traveling', 'He/she was traveling'),
        ('other', 'Other'),
    ]
    child_school_absence_reason = models.CharField(
        max_length=20,
        choices=SCHOOL_ABSENCE_REASON_CHOICES,
        null=True,
        blank=True,
        help_text="If not, why has the child not been to school?"
    )
    child_school_absence_reason_other = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="Specify the reason if 'Other' is selected."
    )
 

    
    # Has the child missed school days in the past 7 days?
    MISSED_SCHOOL_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    missed_school = models.CharField(
        max_length=3,
        choices=MISSED_SCHOOL_CHOICES,
        help_text="Has the child missed school days in the past 7 days? (Mandatory if basic_need_available is not null)"
    )
    
    # If missed school, why did the child miss school?
    MISSED_SCHOOL_REASON_CHOICES = [
        ('sick', 'He/she was sick'),
        ('working', 'He/she was working'),
        ('traveled', 'He/she traveled'),
        ('other', 'Other'),
    ]
    missed_school_reason = models.CharField(
        max_length=20,
        choices=MISSED_SCHOOL_REASON_CHOICES,
        null=True,
        blank=True,
        help_text="Why did the child miss school? (Only applicable if missed_school is 'yes')"
    )
    missed_school_reason_other = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="If 'Other' is selected for why the child missed school, please specify."
    )
    
    # In the past 7 days, has the child worked in the house?
    WORK_IN_HOUSE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    work_in_house = models.CharField(
        max_length=3,
        choices=WORK_IN_HOUSE_CHOICES,
        help_text="In the past 7 days, has the child worked in the house? (Mandatory if child_educated is not null)"
    )
    
    # In the past 7 days, has the child been working on the cocoa farm?
    WORK_ON_COCOA_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    work_on_cocoa = models.CharField(
        max_length=3,
        choices=WORK_ON_COCOA_CHOICES,
        help_text="In the past 7 days, has the child been working on the cocoa farm? (Mandatory if child_work_house is not null)"
    )
    
    # How often has the child worked in the past 7 days?
    WORK_FREQUENCY_CHOICES = [
        ('every_day', 'Every day'),
        ('4-5_days', '4-5 days'),
        ('2-3_days', '2-3 days'),
        ('once', 'Once'),
    ]
    work_frequency = models.CharField(
        max_length=10,
        choices=WORK_FREQUENCY_CHOICES,
        null=True,
        blank=True,
        help_text="How often has the child worked in the past 7 days? (Mandatory if work_in_house or work_on_cocoa is 'yes')"
    )
    
    # Did the enumerator observe the child working in a real situation?
    OBSERVED_WORK_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    observed_work = models.CharField(
        max_length=3,
        choices=OBSERVED_WORK_CHOICES,
        null=True,
        blank=True,
        help_text="Did the enumerator observe the child working in a real situation? (Only applicable if work_in_house is 'yes')"
    )
    
    
 
    TASK_CHOICES = [
        ('collect_fruits', 'Collect and gather fruits, pods, seeds after harvesting'),
        ('extract_cocoa', 'Extracting cocoa beans after shelling by an adult'),
        ('wash_items', 'Wash beans, fruits, vegetables or tubers'),
        ('prepare_germinators', 'Prepare the germinators and pour the seeds into the germinators'),
        ('collect_firewood', 'Collecting firewood'),
        ('measure_distance', 'To help measure distances between plants during transplanting'),
        ('sort_drying', 'Sort and spread the beans, cereals and other vegetables for drying'),
        ('put_cuttings', 'Putting cuttings on the mounds'),
        ('hold_bags', 'Holding bags or filling them with small containers for packaging de produits agricoles'),
        ('cover_products', 'Covering stored agricultural products with tarps'),
        ('shell_dehusk', 'To shell or dehusk seeds, plants and fruits by hand'),
        ('sowing', 'Sowing seeds'),
        ('transplant', 'Transplant or put in the ground the cuttings or plants'),
        ('harvest_legumes', 'Harvesting legumes, fruits and other leafy products (corn, beans, soybeans, various vegetables)'),
        ('none', 'None'),
    ]
    # This field is intended to capture multiple selections.
    # You can store a comma-separated list of the selected task keys.
    performed_tasks = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        help_text="Which of these tasks has the child performed in the last 7 days? "
                  "If multiple, separate using commas."
    )
    # Alternatively, if you install and use django-multiselectfield, you might do:
    # from multiselectfield import MultiSelectField
    # performed_tasks = MultiSelectField(choices=TASK_CHOICES, max_length=500, help_text="Select tasks performed in the last 7 days")
    
    REMUNERATION_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    remuneration_received = models.CharField(
        max_length=3,
        choices=REMUNERATION_CHOICES,
        help_text="Did the child receive remuneration for the activity?"
    )
    
    
    
    # 1. Longest time spent on light duty during a SCHOOL DAY in the last 7 days
    LIGHT_DUTY_DURATION_CHOICES = [
        ('<1', 'Less than 1 hour'),
        ('1-2', '1-2 hour'),
        ('2-3', '2-3 hours'),
        ('3-4', '3-4 hours'),
        ('4-6', '4-6 hours'),
        ('6-8', '6-8 hours'),
        ('>8', 'More than 8 hours'),
        ('na', 'Does not apply'),
    ]
    light_duty_duration_school = models.CharField(
        max_length=10,
        choices=LIGHT_DUTY_DURATION_CHOICES,
        help_text="What was the longest time spent on light duty during a SCHOOL DAY in the last 7 days?"
    )
    
    # 2. Longest time spent on light duty during a NON-SCHOOL DAY in the last 7 days
    LIGHT_DUTY_DURATION_NON_SCHOOL_CHOICES = [
        ('<1', 'Less than 1 hour'),
        ('1-2', '1-2 hour'),
        ('2-3', '2-3 hours'),
        ('3-4', '3-4 hours'),
        ('4-6', '4-6 hours'),
        ('6-8', '6-8 hours'),
        ('>8', 'More than 8 hours'),
    ]
    light_duty_duration_non_school = models.CharField(
        max_length=10,
        choices=LIGHT_DUTY_DURATION_NON_SCHOOL_CHOICES,
        help_text="What was the longest amount of time spent on light duty on a NON-SCHOOL DAY in the last 7 days?"
    )
    
    # 3. Where was this task done?
    TASK_LOCATION_CHOICES = [
        ('family_farm', 'On family farm'),
        ('hired_labour', 'As a hired labourer on another farm'),
        ('school_farms', 'School farms/compounds'),
        ('teachers_farms', 'Teachers farms (during communal labour)'),
        ('church_farms', 'Church farms or cleaning activities'),
        ('community_help', 'Helping a community member for free'),
        ('other', 'Other'),
    ]
    task_location = models.CharField(
        max_length=20,
        choices=TASK_LOCATION_CHOICES,
        help_text="Where was this task done?"
    )
    task_location_other = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="If 'Other' is selected, please specify."
    )
    
    # 4. Total hours spent on light duty during SCHOOL DAYS in the past 7 days
    total_hours_light_work_school = models.IntegerField(
        help_text="How many hours in total did the child spend in light work during SCHOOL DAYS in the past 7 days?"
    )
    
    # 5. Total hours spent on light duty during NON-SCHOOL DAYS in the past 7 days
    total_hours_light_work_non_school = models.IntegerField(
        help_text="How many hours in total did the child spend on light duty during NON-SCHOOL DAYS in the past 7 days?"
    )
    
    # 6. Was the child under supervision of an adult when performing this task?
    SUPERVISION_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    under_supervision = models.CharField(
        max_length=3,
        choices=SUPERVISION_CHOICES,
        help_text="Was the child under supervision of an adult when performing this task?"
    )
    
    def clean(self):
        """Ensure total hours are within a plausible range."""
        if not (0 <= self.total_hours_light_work_school < 1016):
            raise ValidationError("Total hours during SCHOOL DAYS must be between 0 and 1015.")
        if not (0 <= self.total_hours_light_work_non_school < 1016):
            raise ValidationError("Total hours during NON-SCHOOL DAYS must be between 0 and 1015.")
    


# class ChildTaskAssessment12Months(models.Model):
#     child = models.OneToOneField(
#         'ChildSurvey',
#         on_delete=models.CASCADE,
#         related_name='task_assessment_12months',
#         help_text="Link to the main child survey record."
#     )
    
    # List of tasks performed in the last 12 months.
    # If multiple tasks are performed, their keys can be stored as a comma-separated string.
    TASK_CHOICES_12MONTHS = [
        ('collect_fruits', 'Collect and gather fruits, pods, seeds after harvesting'),
        ('extract_cocoa', 'Extracting cocoa beans after shelling by an adult'),
        ('wash_items', 'Wash beans, fruits, vegetables or tubers'),
        ('prepare_germinators', 'Prepare the germinators and pour the seeds into the germinators'),
        ('collect_firewood', 'Collecting firewood'),
        ('measure_distance', 'To help measure distances between plants during transplanting'),
        ('sort_drying', 'Sort and spread the beans, cereals and other vegetables for drying'),
        ('put_cuttings', 'Putting cuttings on the mounds'),
        ('hold_bags', 'Holding bags or filling them with small containers for packaging de produits agricoles'),
        ('cover_products', 'Covering stored agricultural products with tarps'),
        ('shell_dehusk', 'To shell or dehusk seeds, plants and fruits by hand'),
        ('sowing', 'Sowing seeds'),
        ('transplant', 'Transplant or put in the ground the cuttings or plants'),
        ('harvest_legumes', 'Harvesting legumes, fruits and other leafy products (corn, beans, soybeans, various vegetables)'),
        ('none', 'None'),
    ]
    performed_tasks_12months = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        help_text="Which of these tasks has child %rostertitle% performed in the last 12 months? "
                  "If multiple tasks, separate their keys using commas."
    )
    
    # Remuneration received for the activity.
    REMUNERATION_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    remuneration_received_12months = models.CharField(
        max_length=3,
        choices=REMUNERATION_CHOICES,
        help_text="Did the child receive remuneration for the activity %rostertitle%?"
    )
    
    def __str__(self):
        return f"12-Month Task Assessment for Child Survey Record #{self.child.pk}"


# from django.db import models
# from django.core.exceptions import ValidationError

# class ChildLightDutyAssessment12(models.Model):
#     child = models.OneToOneField(
#         'ChildSurvey',
#         on_delete=models.CASCADE,
#         related_name='light_duty_assessment12',
#         help_text="Link to the main child survey record."
#     )
    
    # 1. Longest time spent on light duty during a SCHOOL DAY in the last 7 days
    LIGHT_DUTY_DURATION_SCHOOL_CHOICES = [
        ('<1', 'Less than 1 hour'),
        ('1-2', '1-2 hour'),
        ('2-3', '2-3 hours'),
        ('3-4', '3-4 hours'),
        ('4-6', '4-6 hours'),
        ('6-8', '6-8 hours'),
        ('>8', 'More than 8 hours'),
        ('na', 'Does not apply'),
    ]
    light_duty_duration_school_12 = models.CharField(
        max_length=10,
        choices=LIGHT_DUTY_DURATION_SCHOOL_CHOICES,
        help_text="Longest time spent on light duty during a SCHOOL DAY in the last 7 days."
    )
    
    # 2. Longest time spent on light duty during a NON-SCHOOL DAY in the last 7 days
    LIGHT_DUTY_DURATION_NON_SCHOOL_CHOICES = [
        ('<1', 'Less than 1 hour'),
        ('1-2', '1-2 hour'),
        ('2-3', '2-3 hours'),
        ('3-4', '3-4 hours'),
        ('4-6', '4-6 hours'),
        ('6-8', '6-8 hours'),
        ('>8', 'More than 8 hours'),
    ]
    light_duty_duration_non_school_12 = models.CharField(
        max_length=10,
        choices=LIGHT_DUTY_DURATION_NON_SCHOOL_CHOICES,
        help_text="Longest time spent on light duty during a NON-SCHOOL DAY in the last 7 days."
    )
    
    # 3. Where was this task done?
    TASK_LOCATION_CHOICES = [
        ('family_farm', 'On family farm'),
        ('hired_labour', 'As a hired labourer on another farm'),
        ('school_farms', 'School farms/compounds'),
        ('teachers_farms', 'Teachers farms (during communal labour)'),
        ('church_farms', 'Church farms or cleaning activities'),
        ('community_help', 'Helping a community member for free'),
        ('other', 'Other'),
    ]
    task_location_12 = models.CharField(
        max_length=20,
        choices=TASK_LOCATION_CHOICES,
        help_text="Where was this task done?"
    )
    task_location_other_12 = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="If 'Other' is selected, please specify."
    )
    
    # 4. Total hours spent in light work during SCHOOL DAYS in the past 7 days
    total_hours_light_work_school_12 = models.IntegerField(
        help_text="Total hours spent in light work during SCHOOL DAYS in the past 7 days. Must be between 0 and 1015."
    )
    
    # 5. Total hours spent in light work during NON-SCHOOL DAYS in the past 7 days
    total_hours_light_work_non_school_12 = models.IntegerField(
        help_text="Total hours spent in light work during NON-SCHOOL DAYS in the past 7 days. Must be between 0 and 1015."
    )
    
    # 6. Was the child under supervision of an adult when performing this task?
    SUPERVISION_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    under_supervision_12 = models.CharField(
        max_length=3,
        choices=SUPERVISION_CHOICES,
        help_text="Was the child under supervision of an adult when performing this task?"
    )
    
    def clean(self):
        """Validate that the total hours are within acceptable bounds."""
        if not (0 <= self.total_hours_light_work_school_12 < 1016):
            raise ValidationError("Total hours during SCHOOL DAYS must be between 0 and 1015.")
        if not (0 <= self.total_hours_light_work_non_school_12 < 1016):
            raise ValidationError("Total hours during NON-SCHOOL DAYS must be between 0 and 1015.")
    
    def __str__(self):
        return f"Light Duty Assessment (12) for Child Survey Record #{self.child.pk}"


# from django.db import models
# from django.core.exceptions import ValidationError

# class ChildCocoaFarmHeavyWork(models.Model):
#     child = models.OneToOneField(
#         'ChildSurvey',
#         on_delete=models.CASCADE,
#         related_name='cocoa_farm_heavy_work',
#         help_text="Link to the main child survey record."
#     )
    
    # --- Heavy Tasks on Cocoa Farm in the Last 7 Days ---
    HEAVY_TASK_CHOICES = [
        ('machetes_weeding', 'Use of machetes for weeding or pruning (Clearing)'),
        ('felling_trees', 'Felling of trees'),
        ('burning_plots', 'Burning of plots'),
        ('game_hunting', 'Game hunting with a weapon'),
        ('woodcutter_work', "Woodcutter's work"),
        ('charcoal_production', 'Charcoal production'),
        ('stump_removal', 'Stump removal'),
        ('digging_holes', 'Digging holes'),
        ('sharp_tool_work', 'Working with a machete or any other sharp tool'),
        ('handling_agrochemicals', 'Handling of agrochemicals'),
        ('driving_vehicles', 'Driving motorized vehicles'),
        ('carrying_heavy_loads', 'Carrying heavy loads (Boys: 14-16 years old >15kg / 16-17 years old >20kg; Girls: 14-16 years old >8Kg / 16-17 years old >10Kg)'),
        ('night_work', 'Night work on farm (between 6pm and 6am)'),
        ('none', 'None of the above'),
    ]
    heavy_tasks = models.CharField(
        max_length=500,
        blank=True,
        help_text="Which of the following tasks has the child done in the last 7 days on the cocoa farm? "
                  "If multiple tasks apply, list the keys separated by commas."
    )
    
    # --- Salary ---
    SALARY_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    salary_received = models.CharField(
        max_length=3,
        choices=SALARY_CHOICES,
        help_text="Has the child received a salary for this task?"
    )
    
    # --- Task Location ---
    TASK_LOCATION_CHOICES = [
        ('family_farm', 'On family farm'),
        ('hired_labour', 'As a hired labourer on another farm'),
        ('school_farms', 'School farms/compounds'),
        ('teachers_farms', 'Teachers farms (during communal labour)'),
        ('church_farms', 'Church farms or cleaning activities'),
        ('community_help', 'Helping a community member for free'),
        ('other', 'Other'),
    ]
    task_location = models.CharField(
        max_length=20,
        choices=TASK_LOCATION_CHOICES,
        help_text="Where was this task done?"
    )
    task_location_other = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="If 'Other' is selected, please specify."
    )
    
    # --- Duration Details (CHILDREN OF THE HOUSEHOLD 27 / 37) ---
    # Longest time spent on the task during a SCHOOL DAY in the last 7 days
    DURATION_CHOICES_SCHOOL = [
        ('less_than_1', 'Less than one hour'),
        ('1_hour', '1 hour'),
        ('2_hours', '2 hours'),
        ('3-4_hours', '3-4 hours'),
        ('4-6_hours', '4-6 hours'),
        ('6-8_hours', '6-8 hours'),
        ('more_than_8', 'More than 8 hours'),
        ('does_not_apply', 'Does not apply'),
    ]
    longest_time_school_day = models.CharField(
        max_length=20,
        choices=DURATION_CHOICES_SCHOOL,
        help_text="What was the longest time spent on the task during a SCHOOL DAY in the last 7 days?"
    )
    
    # Longest time spent on the task during a NON-SCHOOL DAY in the last 7 days
    DURATION_CHOICES_NON_SCHOOL = [
        ('less_than_1', 'Less than one hour'),
        ('1-2_hours', '1-2 hour'),
        ('2-3_hours', '2-3 hours'),
        ('3-4_hours', '3-4 hours'),
        ('4-6_hours', '4-6 hours'),
        ('6-8_hours', '6-8 hours'),
        ('more_than_8', 'More than 8 hours'),
    ]
    longest_time_non_school_day = models.CharField(
        max_length=20,
        choices=DURATION_CHOICES_NON_SCHOOL,
        help_text="What was the longest time spent on the task during a NON-SCHOOL DAY in the last 7 days?"
    )
    
    # --- Total Hours Worked ---
    total_hours_school_days = models.IntegerField(
        help_text="How many hours has the child worked on during SCHOOL DAYS in the last 7 days? (0 to 1015 hours)"
    )
    total_hours_non_school_days = models.IntegerField(
        help_text="How many hours has the child been working on during NON-SCHOOL DAYS in the last 7 days? (0 to 1015 hours)"
    )
    
    # --- Supervision ---
    SUPERVISION_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    under_supervision = models.CharField(
        max_length=3,
        choices=SUPERVISION_CHOICES,
        help_text="Was the child under supervision of an adult when performing this task?"
    )
    
    def clean(self):
        """Custom validations for total hours."""
        if not (0 <= self.total_hours_school_days < 1016):
            raise ValidationError("Total hours on school days must be between 0 and 1015.")
        if not (0 <= self.total_hours_non_school_days < 1016):
            raise ValidationError("Total hours on non-school days must be between 0 and 1015.")
    
    def __str__(self):
        return f"Heavy Work Assessment for Child Survey Record #{self.child.pk}"


# from django.db import models

# class ChildCocoaFarmHeavyWork12(models.Model):
#     child = models.OneToOneField(
#         'ChildSurvey',
#         on_delete=models.CASCADE,
#         related_name='cocoa_farm_heavy_work_12',
#         help_text="Link to the main child survey record."
#     )
    
    # Tasks performed in the last 12 months on the cocoa farm.
    HEAVY_TASK_CHOICES_12MONTHS = [
        ('machetes_weeding', 'Use of machetes for weeding or pruning (Clearing)'),
        ('felling_trees', 'Felling of trees'),
        ('burning_plots', 'Burning of plots'),
        ('game_hunting', 'Game hunting with a weapon'),
        ('woodcutter_work', "Woodcutter's work"),
        ('charcoal_production', 'Charcoal production'),
        ('stump_removal', 'Stump removal'),
        ('digging_holes', 'Digging holes'),
        ('sharp_tool_work', 'Working with a machete or any other sharp tool'),
        ('handling_agrochemicals', 'Handling of agrochemicals'),
        ('driving_vehicles', 'Driving motorized vehicles'),
        ('carrying_heavy_loads', 'Carrying heavy loads (Boys: 14-16 years old >15kg / 16-17 years old >20kg; Girls: 14-16 years old >8Kg / 16-17 years old >10Kg)'),
        ('night_work', 'Night work on farm (between 6pm and 6am)'),
        ('none', 'None of the above'),
    ]
    heavy_tasks_12months = models.CharField(
        max_length=500,
        blank=True,
        help_text="Which of the following tasks has the child performed in the last 12 months on the cocoa farm? "
                  "If multiple tasks apply, list the keys separated by commas."
    )
    
    # Salary received for the task.
    SALARY_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    salary_received_12 = models.CharField(
        max_length=3,
        choices=SALARY_CHOICES,
        help_text="Has the child received a salary for this task?"
    )
    
    # Where the task was performed.
    TASK_LOCATION_CHOICES = [
        ('family_farm', 'On family farm'),
        ('hired_labour', 'As a hired labourer on another farm'),
        ('school_farms', 'School farms/compounds'),
        ('teachers_farms', 'Teachers farms (during communal labour)'),
        ('church_farms', 'Church farms or cleaning activities'),
        ('community_help', 'Helping a community member for free'),
        ('other', 'Other'),
    ]
    task_location_12 = models.CharField(
        max_length=20,
        choices=TASK_LOCATION_CHOICES,
        help_text="Where was this task done?"
    )
    task_location_other_12 = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="If 'Other' is selected, please specify."
    )
    
    def __str__(self):
        return f"Cocoa Farm Heavy Work (12 months) for Child Survey Record #{self.child.pk}"


# from django.db import models
# from django.core.exceptions import ValidationError

    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

# class ChildHeavyWorkHealthAssessment(models.Model):
#     child = models.OneToOneField(
#         'ChildSurvey',
#         on_delete=models.CASCADE,
#         related_name='heavy_work_health_assessment',
#         help_text="Link to the main child survey record."
#     )
    
    # --- Heavy Work Duration (Last 7 Days) ---
    LONGEST_TIME_SCHOOL_DAY_CHOICES = [
        ('<1', 'Less than one hour'),
        ('1', '1 hour'),
        ('2', '2 hours'),
        ('3-4', '3-4 hours'),
        ('4-6', '4-6 hours'),
        ('6-8', '6-8 hours'),
        ('>8', 'More than 8 hours'),
        ('na', 'Does not apply'),
    ]
    longest_time_school_day = models.CharField(
        max_length=10,
        choices=LONGEST_TIME_SCHOOL_DAY_CHOICES,
        help_text="Longest time spent on the task during a SCHOOL DAY in the last 7 days."
    )
    
    LONGEST_TIME_NON_SCHOOL_DAY_CHOICES = [
        ('<1', 'Less than one hour'),
        ('1-2', '1-2 hour'),
        ('2-3', '2-3 hours'),
        ('3-4', '3-4 hours'),
        ('4-6', '4-6 hours'),
        ('6-8', '6-8 hours'),
        ('>8', 'More than 8 hours'),
    ]
    longest_time_non_school_day = models.CharField(
        max_length=10,
        choices=LONGEST_TIME_NON_SCHOOL_DAY_CHOICES,
        help_text="Longest time spent on the task during a NON-SCHOOL DAY in the last 7 days."
    )
    
    total_hours_school_days = models.IntegerField(
        help_text="How many hours has the child worked on during SCHOOL DAYS in the last 7 days? (0-1015)"
    )
    total_hours_non_school_days = models.IntegerField(
        help_text="How many hours has the child been working on during NON-SCHOOL DAYS in the last 7 days? (0-1015)"
    )
    
    under_supervision = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        help_text="Was the child under supervision of an adult when performing this task?"
    )
    
    # --- Work Details ---
    WORK_FOR_WHOM_CHOICES = [
        ('parents', "For his/her parents"),
        ('family_not_parents', "For family, not parents"),
        ('family_friends', "For family friends"),
        ('other', "Other"),
    ]
    child_work_who = models.CharField(
        max_length=20,
        choices=WORK_FOR_WHOM_CHOICES,
        help_text="For whom does the child work?"
    )
    child_work_who_other = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="If 'Other' is selected, please specify."
    )
    
    WORK_REASON_CHOICES = [
        ('own_money', "To have his/her own money"),
        ('increase_income', "To increase household income"),
        ('cannot_afford_adult', "Household cannot afford adult's work"),
        ('cannot_find_adult', "Household cannot find adult labor"),
        ('learn_cocoa', "To learn cocoa farming"),
        ('other', "Other"),
        ('does_not_know', "Does not know"),
    ]
    child_work_why = models.CharField(
        max_length=20,
        choices=WORK_REASON_CHOICES,
        help_text="Why does the child work?"
    )
    child_work_why_other = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="If 'Other' is selected for why the child works, please specify (in capital letters)."
    )
    
    # --- Agrochemicals & Farm Exposure ---
    agrochemicals_applied = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        help_text="Has the child ever applied or sprayed agrochemicals on the farm?"
    )
    child_on_farm_during_agro = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        help_text="Was the child on the farm during the application of agrochemicals?"
    )
    
    # --- Injury and Health ---
    suffered_injury = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        help_text="Recently, has the child suffered any injury?"
    )
    
    INJURY_CAUSE_CHOICES = [
        ('playing_outside', "Playing outside"),
        ('household_chores', "Doing household chores"),
        ('helping_farm', "Helping on the farm"),
        ('falling_bicycle', "Falling of a bicycle, scooters or tricycle"),
        ('animal_insect', "Animal or insect bite or scratch"),
        ('fighting', "Fighting with someone else"),
        ('other', "Other"),
    ]
    wound_cause = models.CharField(
        max_length=30,
        choices=INJURY_CAUSE_CHOICES,
        blank=True,
        null=True,
        help_text="How did the child get wounded? (If injured)"
    )
    wound_cause_other = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="If 'Other' is selected, please specify."
    )
    
    WOUND_TIME_CHOICES = [
        ('<week', "Less than a week ago"),
        ('1week-1month', "More than one week and less than a month"),
        ('2-6months', "More than 2 months and less than 6 months"),
        ('>6months', "More than 6 months"),
    ]
    wound_time = models.CharField(
        max_length=20,
        choices=WOUND_TIME_CHOICES,
        blank=True,
        null=True,
        help_text="When was the child wounded? (If injured)"
    )
    
    child_often_pains = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        help_text="Does the child often feel pains or aches?"
    )
    
    # --- Help Received for Health Issues ---
    # For multiple selections, you might use a comma-separated list.
    HELP_CHILD_HEALTH_CHOICES = [
        ('household_adults', "The adults of the household looked after him/her"),
        ('community_adults', "Adults of the community looked after him/her"),
        ('medical_facility', "The child was sent to the closest medical facility"),
        ('no_help', "The child did not receive any help"),
        ('other', "Other"),
    ]
    help_child_health = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="What help did the child receive to get better? (Select all that apply, separated by commas)"
    )
    help_child_health_other = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="If 'Other' is selected above, please specify."
    )
    child_photo = models.ImageField(
        upload_to='child_photos/',
        blank=True,
        null=True,
        help_text="Upload a photo of the child (if available)."
    )
    
    def clean(self):
        errors = {}
        if not (0 <= self.total_hours_school_days < 1016):
            errors['total_hours_school_days'] = "Total hours on school days must be between 0 and 1015."
        if not (0 <= self.total_hours_non_school_days < 1016):
            errors['total_hours_non_school_days'] = "Total hours on non-school days must be between 0 and 1015."
        if errors:
            raise ValidationError(errors)
    
    def __str__(self):
        return f"Heavy Work & Health Assessment for Child Survey Record #{self.child.pk}"



####################################################################################################
# Child Remediation Assessment
####################################################################################################

# from django.db import models

class ChildRemediationTbl(models.Model):
    # Link to the main survey record (e.g., a FarmerSurvey or HouseholdSurvey)
    # survey = models.OneToOneField(
    #     'FarmerSurvey',  # Replace with your appropriate survey model name
    #     on_delete=models.CASCADE,
    #     related_name='child_remediation',
    #     help_text="Link to the main survey record. This section is shown if consent==1, farmer_available==1, and date is set."
    # )
    cover = models.OneToOneField(
        Cover_tbl,
        on_delete=models.CASCADE,
        related_name='child_remediation',
        null=True
    )
    
    # Question 1: Do you owe fees for the school of the children living in your household?
    SCHOOL_FEES_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    school_fees_owed = models.CharField(
        max_length=3,
        choices=SCHOOL_FEES_CHOICES,
        help_text="Do you owe fees for the school of the children living in your household?"
    )
    
    # Question 2: What should be done for the parent to stop involving their children in child labour?
    PARENT_REMEDIATION_CHOICES = [
        ('child_protection', 'Child protection and parenting education'),
        ('school_kits', 'School kits support'),
        ('iga_support', 'IGA support'),
        ('other', 'Other'),
    ]
    parent_remediation = models.CharField(
        max_length=20,
        choices=PARENT_REMEDIATION_CHOICES,
        help_text="What should be done for the parent to stop involving their children in child labour?"
    )
    parent_remediation_other = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="If 'Other' is selected, specify in capital letters."
    )
    
    # Question 3: What can be done for the community to stop involving the children in child labour?
    COMMUNITY_REMEDIATION_CHOICES = [
        ('community_education', 'Community education on child labour'),
        ('school_building', 'Community school building'),
        ('school_renovation', 'Community school renovation'),
        ('other', 'Other'),
    ]
    community_remediation = models.CharField(
        max_length=30,
        choices=COMMUNITY_REMEDIATION_CHOICES,
        help_text="What can be done for the community to stop involving the children in child labour?"
    )
    community_remediation_other = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="If 'Other' is selected, specify in capital letters."
    )
    
    def __str__(self):
        return f"Child Remediation Assessment for Survey Record #{self.survey.pk}"




####################################################################################################
# Household Sensitization Assessment
####################################################################################################

# from django.db import models
# from django.core.validators import MinValueValidator

  

class HouseholdSensitizationTbl(models.Model):
    
    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    # Link to the main survey record.
    # survey = models.OneToOneField(
    #     'FarmerSurvey',  # Replace with the appropriate main survey model name.
    #     on_delete=models.CASCADE,
    #     related_name='household_sensitization',
    #     help_text="Link to the main survey record. This section applies if farmer_available==1 or farmer_unit is not null."
    # )
    cover = models.OneToOneField(
        Cover_tbl,
        on_delete=models.CASCADE,
        related_name='household_sensitization',
        null=True
    )
    
    # Sensitization on Good Parenting.
    sensitized_good_parenting = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        help_text="Have you sensitized the household members on Good Parenting? (This is mandatory.)"
    )
    
    # Sensitization on Child Protection.
    sensitized_child_protection = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        help_text="Have you sensitized the household members on Child Protection? (This is mandatory.)"
    )
    
    # Sensitization on Safe Labour Practices.
    sensitized_safe_labour = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        help_text="Have you sensitized the household members on Safe Labour Practices? (This is mandatory.)"
    )
    
    # Number of female adults present during sensitization.
    number_of_female_adults = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="How many female adults were present during the sensitization? (Must be at least 1.)"
    )
    
    # Number of male adults present during sensitization.
    number_of_male_adults = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="How many male adults were present during the sensitization? (Must be at least 1.)"
    )
    
    # Whether a picture of the respondent and enumerator was taken.
    picture_of_respondent = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        help_text="Can you take a picture of the respondent and yourself?"
    )
    
    # Picture of the sensitization in progress (to be taken if remediation_consentement_pho == 1).
    picture_sensitization = models.ImageField(
        upload_to='sensitization/',
        blank=True,
        null=True,
        help_text="Please take a picture of the sensitization being implemented with the family and the child."
    )
    
    # Observations regarding the reaction from the parents.
    feedback_observations = models.TextField(
        blank=True,
        null=True,
        help_text="What are your observations regarding the reaction from the parents on the sensitization provided?"
    )
    
    def __str__(self):
        return f"Sensitization Assessment for Survey Record #{self.survey.pk}"



####################################################################################################
# End of Collection
####################################################################################################


# from django.db import models

class EndOfCollection(models.Model):
    cover = models.OneToOneField(
        Cover_tbl,
        on_delete=models.CASCADE,
        related_name='end_of_collection',
        null=True
    )
    
    # Enumerator feedback is mandatory.
    feedback_enum = models.TextField(
        help_text="Feedback from enumerator. This field is required."
    )
    
    # Picture of Respondent (required if farmer_available == True).
    picture_of_respondent = models.ImageField(
        upload_to='respondent_pictures/',
        blank=True,
        null=True,
        help_text="Picture of the respondent. Required if farmer_available is True."
    )
    
    # Signature of Producer (required if farmer_available == True).
    signature_producer = models.ImageField(
        upload_to='producer_signatures/',
        blank=True,
        null=True,
        help_text="Signature of the producer. Required if farmer_available is True."
    )
    
    # End GPS of survey (required if sp6_code, farmer_code, and client are not null).
    end_gps = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="End GPS coordinates of the survey. Required if sp6_code, farmer_code, and client are set."
    )
    
    # End time of survey (required if sp6_code, farmer_code, and client are not null).
    end_time = models.DateTimeField(
        blank=True,
        null=True,
        help_text="End time of the survey. Required if sp6_code, farmer_code, and client are set."
    )
    
    def __str__(self):
        return f"End of Collection for Survey Record #{self.survey.pk}"
