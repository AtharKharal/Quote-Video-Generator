from vid_publisher import VideoPublisher

input_dict = {
  "caption": """William Shakespeare was an English playwright, poet, and actor, widely regarded as the greatest writer in the English language and the greatest dramatist in history. He was born in 1564 in Stratford-upon-Avon, England, and died in 1616.

Shakespeare wrote about 39 plays, 154 sonnets, and several narrative poems. His works explore universal themes such as love, ambition, power, jealousy, and human nature. His plays are generally divided into three main categories: tragedies, comedies, and histories.

Some of his most famous plays include Hamlet, Romeo and Juliet, Macbeth, Othello, and King Lear. His writing greatly influenced English literature and the modern English language, introducing many new words and expressions still used today.

Even centuries after his death, Shakespeare’s works continue to be studied, performed, and admired all over the world.

#poetry #literature #shakespeare""",

    "file_path": "./output.mp4"
}

vidPublisher = VideoPublisher(input_dict["caption"], input_dict["file_path"])

if __name__ == "__main__":
    vidPublisher.publish_video()