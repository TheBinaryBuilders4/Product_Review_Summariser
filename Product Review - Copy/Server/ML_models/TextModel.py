from transformers import AutoModel, AutoConfig, AutoTokenizer
import torch
import torch.nn as nn

CONFIG = {"seed": 2022,
            "epochs": 3,
            "model_name": "microsoft/deberta-v3-base",
            "train_batch_size": 8,
            "valid_batch_size": 16,
            "max_length": 512,
            "learning_rate": 1e-5,
            "scheduler": 'CosineAnnealingLR',
            "min_lr": 1e-6,
            "T_max": 500,
            "weight_decay": 1e-6,
            "n_fold": 3,
            "n_accumulate": 1,
            "num_classes": 3,
            "device": torch.device("cuda:0" if torch.cuda.is_available() else "cpu"),
            "competition": "amazon-reviews-dataset",
            "_wandb_kernel": "react",
            }

CONFIG["tokenizer"] = AutoTokenizer.from_pretrained(CONFIG['model_name'])


class TextModel(nn.Module):
    def __init__(self, model_name):
        super(TextModel, self).__init__()
        self.model = AutoModel.from_pretrained(model_name)
        self.config = AutoConfig.from_pretrained(model_name)
        self.drop = nn.Dropout(p=0.2)
        self.pooler = MeanPooling()
        self.fc = nn.Linear(self.config.hidden_size, CONFIG['num_classes'])
        
    def forward(self, ids, mask):        
        out = self.model(input_ids=ids,attention_mask=mask,
                         output_hidden_states=False)
        out = self.pooler(out.last_hidden_state, mask)
        out = self.drop(out)
        outputs = self.fc(out)
        return outputs

class MeanPooling(nn.Module):
    """ The MeanPooling class inherits from the nn.Module class which is the base class for all neural network modules in PyTorch. """
    def __init__(self):
        super(MeanPooling, self).__init__()
        # In above line _init_() is called to initialize the nn.Module parent class.

    def forward(self, last_hidden_state, attention_mask):

        # attention_mask => (batch_size, sequence_length)
        # last_hidden_state represents the output of the transformer model, which is a 3D tensor of shape (batch_size, sequence_length, hidden_size).

        # First, the attention_mask is expanded to match the size of the last_hidden_state:
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(last_hidden_state.size()).float() # => (batch_size, sequence_length, hidden_size).
        # The resulting tensor is of shape (batch_size, sequence_length, hidden_size).
        #  where each [PAD] token is represented by a vector of zeros, and all other tokens are represented by vectors of ones.

        # Then, the last_hidden_state is multiplied by the expanded mask to zero out the embeddings of the [PAD] tokens:
        sum_embeddings = torch.sum(last_hidden_state * input_mask_expanded, 1)
        # This line computes the sum of the input_mask_expanded along the sequence_length dimension.
        # This sum represents the number of actual (non-padding) tokens in each sequence of the batch.

        # The sum of the mask values is then computed for each sentence:
        # Result: A 2D tensor of shape (batch_size, hidden_size), where each value represents the number of actual tokens (excluding padding tokens) in the corresponding sentence.
        sum_mask = input_mask_expanded.sum(1) #=> (batch_size, hidden_size)

        """ In above line, the sum function with argument 1 is called on input_mask_expanded to compute the sum along the sequence_length dimension. Essentially, this operation is adding up all the 1s for each sequence in the batch, which gives us the number of actual tokens (i.e., non-padding tokens) in each sequence.
        So, sum_mask is a 2D tensor of shape (batch_size, hidden_size), where each value represents the number of actual tokens in the corresponding sequence.

        This is a crucial step in calculating the mean embeddings for each sequence. By summing the mask values, we essentially count the number of valid (non-padding) tokens in each sequence. This count is later used as the denominator when calculating the mean (i.e., sum of token embeddings / number of tokens).

        By only considering non-padding tokens, we ensure the mean embeddings accurately represent the sequence, rather than being skewed by padding tokens that carry no meaningful information.
        """

        # a lower limit is set on the sum_mask values to avoid division by zero:
        # Result: The same tensor as sum_mask, but any value that was originally zero is now 1e-9.
        sum_mask = torch.clamp(sum_mask, min=1e-9)

        #Finally, the mean of the embeddings is computed by dividing the sum of the embeddings by the number of actual tokens:
        mean_embeddings = sum_embeddings / sum_mask

        # Result: A 2D tensor of shape (batch_size, hidden_size), representing the sentence-level embeddings computed as the mean of the token-level embeddings (ignoring padding tokens).
        return mean_embeddings