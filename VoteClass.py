import time
import FunctionFile

class VoteKick_struct:
    def __init__(self, VotedUser, VotingUser, CurrentChannelSize):
        self.timeVoteKickStarted = time.time()
        self.VotedUser = VotedUser
        self.VotingUserList = [VotingUser]
        self.VotedUserSize = len(self.VotingUserList)
        self.CurrentChannelSize = CurrentChannelSize
        self.NeededVoted = FunctionFile.Ciel(3*self.CurrentChannelSize, 4)
        print("Vote Kick started by - " + VotingUser.name + " against - " + VotedUser.name + "@ time " + str(time.time()))

    def has5minpassed(self):
        #print("Current Time = " + str(time.time()))
        if self.timeVoteKickStarted + 300 < time.time():
            return True
        else:
            return False

    def refreshNeededVoteSize(self, CurrentChannelSize):
        self.NeededVoted = FunctionFile.Ciel(3 * self.CurrentChannelSize, 4)

    def hasNeededVoteSizeBeenMet(self, CurrentChannelSize):
        self.CurrentChannelSize = CurrentChannelSize
        self.NeededVoted = FunctionFile.Ciel(3 * self.CurrentChannelSize, 4)
        self.VotedUserSize = len(self.VotingUserList)
        if self.NeededVoted <= self.VotedUserSize:
            return True
        else:
            return False

    def addVotingUser(self,VotingUser, CurrentChannelSize):
        self.CurrentChannelSize = CurrentChannelSize
        if VotingUser in self.VotingUserList:
            print("User" + VotingUser.name + " has already voted for " + self.VotedUser.name)
        else:
            self.VotingUserList.append(VotingUser)
            print("User" + VotingUser.name + " has voted for " + self.VotedUser.name)
            self.VotedUserSize = len(self.VotingUserList)

    def removeUserWhoNoLongerAreInChannel(self, VoiceChannelUserList):
            for voter in self.VotingUserList:
                if voter not in VoiceChannelUserList:
                    print("User" + voter.name + " has already vote for " + self.VotedUser.name)
                    self.VotingUserList.remove(voter)
            self.VotedUserSize = len(self.VotingUserList)