import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class ActorCritic(nn.Module):
    def __init__(self, learning_rate, input_shape, n_actions):
        super(ActorCritic, self).__init__()
        self.input_shape = input_shape
        self.n_actions = n_actions

        self.conv = nn.Sequential(
            nn.Conv2d(self.input_shape[0], 32, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1),
            nn.ReLU()
        )

        conv_out_size = self._get_conv_out(self.input_shape)

        self.mu = nn.Sequential(
            nn.Linear(conv_out_size, 512),
            nn.ReLU(),
            nn.Linear(512, n_actions),
            nn.Tanh()
        )

        self.var = nn.Sequential(
            nn.Linear(conv_out_size, 512),
            nn.ReLU(),
            nn.Linear(512, n_actions),
            nn.Softplus()
        )

        self.value = nn.Sequential(
            nn.Linear(conv_out_size, 512),
            nn.ReLU(),
            nn.Linear(512, 1)
        )


        self.optimiser = optim.Adam(self.parameters(), lr=learning_rate)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.to(self.device)

    def _get_conv_out(self, shape): # calculates the size of the output of the CNN
        o = self.conv(torch.zeros(1,*shape)) # sends through a zero vector the same shape as the state vector passed in
        return int(np.prod(o.size()))
                                                                                                                                                                                
    def forward(self, state):
        state = torch.tensor([state], dtype=torch.float).cuda()
        conv_out = self.conv(state).view(1, -1) # passes state through CNN and reshapes
        return self.mu(conv_out), self.var(conv_out), self.value(conv_out)

