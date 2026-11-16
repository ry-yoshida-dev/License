from enum import Enum


class UseKind(Enum):
    """
    Kind of use of a work that a license permits, restricts, or prohibits.

    Attributes
    ----------
    COMMERCIAL_USE
        Use in commercial products, services, or business.
    NON_RESEARCH_USE
        Use for purposes other than scientific research or academic development.
    AI_TRAINING
        Training or fine-tuning machine learning models on the work.
    MODIFICATION
        Editing, processing, or adapting the work, including for private use.
    REDISTRIBUTION
        Making copies of the work available to third parties.
    MODIFIED_REDISTRIBUTION
        Making adaptations of the work available to third parties; mere format shifts are not adaptations.
    NETWORK_SERVICE
        Letting third parties use software or a model that runs the work over a network, as a hosted service.
    """

    COMMERCIAL_USE = "commercial_use"
    NON_RESEARCH_USE = "non_research_use"
    AI_TRAINING = "ai_training"
    MODIFICATION = "modification"
    REDISTRIBUTION = "redistribution"
    MODIFIED_REDISTRIBUTION = "modified_redistribution"
    NETWORK_SERVICE = "network_service"
