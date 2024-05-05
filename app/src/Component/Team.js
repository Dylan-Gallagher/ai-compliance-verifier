import React from 'react';
import './Team.css';

const teamMembers = [
    {
      name: "Liz Chow",
      role: "Project Manager and Frontend Lead",
      email: "liz@example.com",
      description: "3rd Year CSB",
    },
    {
        name: "Faith Olopade",
        role: "Team Lead",
        email: "faith@example.com",
        description: "3rd Year ICS",
    },
    {
      name: "Rowan Barr",
      role: "Backend Lead",
      email: "rowan@example.com",
      description: "3rd Year ICS",
    },
    {
        name: "Allan Nastin",
        role: "Github Manager",
        email: "allan@example.com",
        description: "3rd Year ICS",
    },
    {
        name: "Tadgh Heneghan",
        role: "Kanban Board Manager",
        email: "tadgh@example.com",
        description: "3rd Year ICS",
    },
    {
        name: "Radnitz Oriasotie",
        role: "Backend Developer",
        email: "radnitz@example.com",
        description: "3rd Year ICS",
    },
    {
        name: "Bianca Ivascu",
        role: "Frontend Developer",
        email: "bianca@example.com",
        description: "2nd Year ICS",
    },
    {
        name: "Travis Yusuf",
        role: "Frontend Developer",
        email: "travis@example.com",
        description: "2nd Year CSB",
    },
    {
        name: "Daniel Fitzgerald",
        role: "Backend Developer",
        email: "daniel@example.com",
        description: "2nd Year ICS",
    },
    {
        name: "Dylan Gallagher",
        role: "Backend Developer",
        email: "dylan@example.com",
        description: "2nd Year ICS",
    },
    {
        name: "William Chen",
        role: "Backend Developer",
        email: "william@example.com",
        description: "2nd Year ICS",
    },
  ];

function Team() {
    return (
        <div className="about-section">
            <h1>About Us</h1>
            <p>Some information about who we are and what we do.</p>

            <h2 style={{ textAlign: 'center' }}>Our Team</h2>
            <div className="row">
                {teamMembers.map(member => (
                <div className="column" key={member.name}>
                    <div className="card">
                        <div className="container">
                            <h2>{member.name}</h2>
                            <p className="title">{member.role}</p>
                            <p>{member.description}</p>
                            <p>Email</p>
                            <p><button className="button" onClick={() => window.location.href = `mailto:${member.email}`}>
                              Contact
                            </button></p>
                        </div>
                    </div>
                </div>
            ))}
            </div>
        </div>
    );
}

export default Team;
