import React from 'react';
import { MapPin, Briefcase, DollarSign, TrendingUp } from 'lucide-react';

const JobCard = ({ job }) => {
  const matchPercentage = (job.similarity_score * 100).toFixed(1);
  
  const getMatchColor = (score) => {
    if (score >= 0.7) return 'text-green-600 bg-green-50';
    if (score >= 0.5) return 'text-yellow-600 bg-yellow-50';
    return 'text-orange-600 bg-orange-50';
  };

  return (
    <div className="card hover:scale-[1.02] transition-transform cursor-pointer">
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="text-xl font-bold text-gray-800">{job.title}</h3>
          <p className="text-blue-600 font-semibold">{job.company}</p>
        </div>
        
        <div className={`px-3 py-1 rounded-full ${getMatchColor(job.similarity_score)}`}>
          <div className="flex items-center space-x-1">
            <TrendingUp className="h-4 w-4" />
            <span className="font-bold">{matchPercentage}%</span>
          </div>
        </div>
      </div>

      <div className="space-y-2 mb-4">
        {job.location && (
          <div className="flex items-center space-x-2 text-gray-600">
            <MapPin className="h-4 w-4" />
            <span>{job.location}</span>
          </div>
        )}
        
        <div className="flex items-center space-x-2 text-gray-600">
          <Briefcase className="h-4 w-4" />
          <span>{job.job_type}</span>
        </div>
        
        {job.salary_range && (
          <div className="flex items-center space-x-2 text-gray-600">
            <DollarSign className="h-4 w-4" />
            <span>{job.salary_range}</span>
          </div>
        )}
      </div>

      <p className="text-gray-700 text-sm line-clamp-3 mb-4">
        {job.description}
      </p>

      {job.matched_skills && job.matched_skills.length > 0 && (
        <div className="border-t pt-3">
          <p className="text-sm font-semibold text-gray-700 mb-2">Matched Skills:</p>
          <div className="flex flex-wrap gap-2">
            {job.matched_skills.slice(0, 5).map((skill, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium"
              >
                {skill}
              </span>
            ))}
            {job.matched_skills.length > 5 && (
              <span className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-xs">
                +{job.matched_skills.length - 5} more
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default JobCard;